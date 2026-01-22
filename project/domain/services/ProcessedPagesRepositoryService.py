from typing import Tuple

from project.domain.repositories import IPageStateRepository
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ProcessedPagesRepositoryService:
    """
    A domain service that manages the state of loaded pages.
    """

    def __init__(self, repository: IPageStateRepository):
        self.repository = repository

    async def add_url(self, slug: str, page: int) -> None:
        """
        Adds the URL to the page state storage.
        """

        await self.repository.add_url(slug, page)

    async def get_loaded_pages(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        return await self.repository.get_data_from_category(slug)
