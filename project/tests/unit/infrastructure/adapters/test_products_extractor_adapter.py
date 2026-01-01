from project.domain.services.products_extractor import ProductsExtractor
from project.infrastructure.adapters.products_extractor_adapter import ProductsExtractorAdapter


def test_adapter_with_str():
    extractor = ProductsExtractor()
    adapter = ProductsExtractorAdapter(extractor)

    html = '''
        window.INITIAL_STATE["plp"] = {
            "productsData": [{"id": 10}]
        };
    '''

    products = adapter.create_products_list(html)
    assert products == [{"id": 10}]


def test_adapter_with_path(tmp_path):
    extractor = ProductsExtractor()
    adapter = ProductsExtractorAdapter(extractor)

    file = tmp_path / "page.html"
    file.write_text(
        'window.INITIAL_STATE["plp"] = {"productsData": [{"id": 99}]};',
        encoding="utf-8"
    )

    products = adapter.create_products_list(file)
    assert products == [{"id": 99}]
