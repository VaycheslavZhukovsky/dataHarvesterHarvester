from typing import Protocol, List


class IProductsExtractor(Protocol):
    """
    Интерфейс чистого парсера HTML → products list.
    Принимает только строку HTML.
    """
    def create_products_list_from_str(self, html: str) -> List[dict]:
        ...
