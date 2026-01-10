from typing import Protocol, List


class IProductsExtractor(Protocol):
    """
    Clean HTML parser interface → products list.
    It accepts only an HTML string.
    """
    def create_products_list_from_str(self, html: str) -> List[dict]:
        ...
