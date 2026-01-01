import pytest
from project.domain.services.products_extractor import ProductsExtractor


@pytest.fixture
def extractor():
    return ProductsExtractor()


def test_unbalanced_json_braces(extractor):
    html = 'window.INITIAL_STATE["plp"] = {"productsData": [1, 2, 3]'
    with pytest.raises(ValueError):
        extractor.extract_json_from_html_str(html)


def test_unbalanced_array_brackets(extractor):
    json_text = '{"productsData": [1, 2, 3}'
    with pytest.raises(ValueError):
        extractor.extract_products_data(json_text)


def test_empty_html(extractor):
    with pytest.raises(ValueError):
        extractor.create_products_list_from_str("")
