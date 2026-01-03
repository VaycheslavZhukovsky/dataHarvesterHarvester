from typing import Tuple

from project.domain.repositories.IPageStateRepository import IPageStateRepository


class FakePageStateRepository(IPageStateRepository):
    """
    Временная заглушка вместо БД.
    """

    def __init__(self):
        # ключ: url, значение: список обработанных страниц
        self._storage = {
            "https://lemanapro.ru/catalogue/oboi-pod-pokrasku/": [1, 2, 3]
        }

    def get_data_from_category(self, url: str) -> Tuple[int, Tuple[int, ...]]:
        pages = self._storage.get(url, [])
        all_pages = 5
        return all_pages, tuple(pages)
