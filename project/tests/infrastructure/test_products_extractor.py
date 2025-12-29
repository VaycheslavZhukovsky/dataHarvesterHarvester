import pytest

from project.infrastructure.parsers.products_extractor import ProductsExtractor


# ---------------------------------------------------------
# ТЕСТЫ extract_json_from_garbage
# ---------------------------------------------------------
def test_extract_json_from_garbage_ok():
    extractor = ProductsExtractor()
    text = 'garbage... {"a":1,"b":{"c":2}} trailing...'
    result = extractor.extract_json_from_garbage(text)
    assert result == '{"a":1,"b":{"c":2}}'


def test_extract_json_from_garbage_no_brace():
    extractor = ProductsExtractor()
    with pytest.raises(ValueError, match="No '{' found"):
        extractor.extract_json_from_garbage("just text without json")


def test_extract_json_from_garbage_unbalanced():
    extractor = ProductsExtractor()
    broken = '{"a":1,"b":{"c":2}'   # Нет финальной }
    with pytest.raises(ValueError, match="JSON braces not balanced"):
        extractor.extract_json_from_garbage(broken)


# ---------------------------------------------------------
# ТЕСТЫ extract_products_data
# ---------------------------------------------------------
def test_extract_products_data_ok():
    extractor = ProductsExtractor()
    json_text = '{"productsData":[{"id":1},{"id":2}],"other":123}'
    result = extractor.extract_products_data(json_text)
    assert result == '[{"id":1},{"id":2}]'


def test_extract_products_data_missing_key():
    extractor = ProductsExtractor()
    with pytest.raises(ValueError, match="productsData not found"):
        extractor.extract_products_data('{"other":[1,2,3]}')


def test_extract_products_data_missing_bracket():
    extractor = ProductsExtractor()
    with pytest.raises(ValueError, match="array '\\[' not found"):
        extractor.extract_products_data('{"productsData": 123}')


def test_extract_products_data_not_closed():
    extractor = ProductsExtractor()
    with pytest.raises(ValueError, match="not closed"):
        extractor.extract_products_data('{"productsData":[1,2,3}')


# ---------------------------------------------------------
# ТЕСТЫ extract_json_from_html
# ---------------------------------------------------------
def test_extract_json_from_html_ok(tmp_path):
    extractor = ProductsExtractor()
    html_content = '''
        <script>
        window.INITIAL_STATE["plp"] = {"productsData":[{"id":10}]};
        </script>
    '''
    file = tmp_path / "test.html"
    file.write_text(html_content, encoding="utf-8")

    json_str = extractor.extract_json_from_html(file)
    assert '{"productsData":[{"id":10}]}' in json_str


def test_extract_json_from_html_no_marker(tmp_path):
    extractor = ProductsExtractor()
    file = tmp_path / "test.html"
    file.write_text("<html>No state here</html>", encoding="utf-8")

    assert extractor.extract_json_from_html(file) is None


# ---------------------------------------------------------
# ТЕСТЫ create_products_list
# ---------------------------------------------------------
def test_create_products_list_ok(tmp_path):
    extractor = ProductsExtractor()
    html = '''
    <script>
    window.INITIAL_STATE["plp"] = {"productsData":[{"id":1}, {"id":2, "name":"x"}]};
    </script>
    '''
    file = tmp_path / "page.html"
    file.write_text(html, encoding="utf-8")

    result = extractor.create_products_list(file)
    assert isinstance(result, list)
    assert result == [{"id": 1}, {"id": 2, "name": "x"}]


def test_create_products_list_not_found(tmp_path):
    extractor = ProductsExtractor()
    file = tmp_path / "page.html"
    file.write_text("<html></html>", encoding="utf-8")

    with pytest.raises(ValueError, match="not found"):
        extractor.create_products_list(file)
