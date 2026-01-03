from typing import Tuple

from project.domain.repositories import IPageStateRepository


class PageStateService:
    """
    Доменный сервис, который получает информацию о загруженных страницах.
    """

    def __init__(self, repository: IPageStateRepository):
        self.repository = repository

    def get_loaded_pages(self, url: str) -> Tuple[int, Tuple[int, ...]]:
        return self.repository.get_data_from_category(url)
