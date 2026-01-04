from typing import Tuple

from project.domain.repositories import IPageStateRepository


class PageStateService:
    """
    Доменный сервис, который управляет состоянием загруженных страниц.
    """

    def __init__(self, repository: IPageStateRepository):
        self.repository = repository

    def add_url(self, url: str) -> None:
        """
        Добавляет URL в хранилище состояния страниц.
        """
        self.repository.add_url(url)

    def get_loaded_pages(self, url: str) -> Tuple[int, Tuple[int, ...]]:
        """
        Возвращает:
        - total_pages (заглушка или реальное значение)
        - tuple обработанных страниц
        """
        return self.repository.get_data_from_category(url)
