from typing import Tuple

from project.domain.repositories import IPageStateRepository
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ProcessedPagesService:
    """
    Доменный сервис, который управляет состоянием загруженных страниц.
    """

    def __init__(self, repository: IPageStateRepository):
        self.repository = repository

    async def add_url(self, slug: str, page: int) -> None:
        """
        Добавляет URL в хранилище состояния страниц.
        """

        await self.repository.add_url(slug, page)

    async def get_loaded_pages(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        """
        Возвращает:
        - total_pages (заглушка или реальное значение)
        - tuple обработанных страниц
        """
        return await self.repository.get_data_from_category(slug)
