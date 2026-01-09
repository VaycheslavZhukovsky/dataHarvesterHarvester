import pytest

from project.infrastructure.exceptions.parsing_errors import JsonExtractionError, JsonBlockNotFoundError, \
    ProductsDataMalformedError
from project.infrastructure.parsers.ProductsExtractorFromHtml import ProductsExtractorFromHtml


@pytest.fixture
def extractor():
    return ProductsExtractorFromHtml()


def test_unbalanced_json_braces(extractor):
    html = 'window.INITIAL_STATE["plp"] = {"productsData": [1, 2, 3]'
    with pytest.raises(JsonExtractionError):
        extractor.extract_json_from_html_str(html)


def test_unbalanced_array_brackets(extractor):
    json_text = '{"productsData": [1, 2, 3}'
    with pytest.raises(ProductsDataMalformedError):
        extractor.extract_products_data(json_text)


def test_empty_html(extractor):
    with pytest.raises(JsonBlockNotFoundError):
        extractor.create_products_list_from_str("")
