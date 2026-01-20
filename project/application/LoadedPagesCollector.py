import asyncio
from typing import List, Tuple

from project.domain.services.ProcessedPagesService import ProcessedPagesService
from project.domain.value_objects.UrlParts import UrlParts
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class LoadedPagesCollector:
    """
    Собирает информацию о загруженных страницах для списка UrlParts.
    Работает конкурентно.
    """

    def __init__(self, processed_pages_service: ProcessedPagesService):
        self.processed_pages = processed_pages_service

    async def collect(self, url_parts_list: List[UrlParts]) -> Tuple[List[UrlParts], List[UrlParts]]:
        """
        Возвращает:
        - urls_with_pages: список UrlParts, у которых есть загруженные страницы
        - urls_without_pages: список UrlParts, у которых all_pages == 0
        """

        tasks = [
            asyncio.create_task(self.processed_pages.get_loaded_pages(parts.segments[1]))
            for parts in url_parts_list
        ]

        results = await asyncio.gather(*tasks)

        urls_with_pages: List[Tuple[UrlParts, tuple]] = []
        urls_without_pages: List[UrlParts] = []

        for parts, (all_pages, all_processed_pages) in zip(url_parts_list, results):
            if all_pages > 0:
                logger.info(f"{parts}: {all_pages} pages, processed={all_processed_pages}")
                urls_with_pages.append((parts, (all_pages, all_processed_pages)))
            else:
                urls_without_pages.append(parts)

        return urls_with_pages, urls_without_pages
