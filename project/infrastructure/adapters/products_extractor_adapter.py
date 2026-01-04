from pathlib import Path
from typing import List, Union

from project.infrastructure.parsers.products_extractor import ProductsExtractor
from project.infrastructure.adapters.file_html_reader import FileHtmlReader


class ProductsExtractorAdapter:
    """
    Адаптер, который позволяет использовать Path или str.
    """

    def __init__(self, extractor: ProductsExtractor):
        self.extractor = extractor

    def create_products_list(self, html: Union[str, Path]) -> List[dict]:
        if isinstance(html, Path):
            html = FileHtmlReader.read(html)

        return self.extractor.create_products_list_from_str(html)
