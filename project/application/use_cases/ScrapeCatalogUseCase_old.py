import asyncio

from project.domain.exceptions.ProductError import ValueObjectProductValidationError
from project.infrastructure.exceptions.db_exceptions import CategoryNotFoundError, DatabaseOperationError, \
    DatabaseConnectionError
from project.infrastructure.exceptions.parsing_errors import ParsingError
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ScrapeCatalogUseCase:
    def __init__(
            self,
            loader,
            processed_pages,
            first_page_load_category_uc,
            recovery_processed_data_category_uc,
            scraper_page_uc,
            url_parts,
            page_category_total_products,
            page_product_repository,
            retry_policy,
    ):
        self.loader = loader
        self.processed_pages = processed_pages
        self.url_parts = url_parts
        self.page_category_total_products = page_category_total_products
        self.page_product_repository = page_product_repository
        self.retry_policy = retry_policy

        self.first_page_load_category_uc = first_page_load_category_uc
        self.recovery_processed_data_category_uc = recovery_processed_data_category_uc

        self.scraper_page_uc = scraper_page_uc

    async def execute(self, url: str):
        logger.info(f"Starting catalog scraping for URL: {url}")

        slug = self.url_parts.from_url(url).segments[1]

        try:
            all_pages, processed_pages = await self.processed_pages.get_loaded_pages(slug)

            await self.loader.start()

            if not processed_pages:
                paginator = await self.first_page_load_category_uc.get_total_products(url)
                total_products = paginator.total_products
                slug = paginator.parts.segments[1]
                await self.page_category_total_products.update_total_products(slug, total_products)
            else:
                paginator = self.recovery_processed_data_category_uc.assemble_paginator(url, all_pages, processed_pages)

            while True:
                page_url = paginator.next_url()
                if not page_url:
                    break
                page = paginator.current_page()
                slug = paginator.parts.segments[1]
                logger.info(f"Scraping page: {page_url}")

                try:
                    entities = await self.scraper_page_uc.get_all_products(page_url)
                    self.retry_policy.register_success()

                except ParsingError:
                    self.retry_policy.register_failure()

                    if not self.retry_policy.should_retry():
                        logger.error("3 ошибки подряд. Прокидываю исключение дальше.")
                        await self.loader.close()
                        raise

                    logger.warning(
                        f"Ошибка парсинга. Попытка {self.retry_policy.current} из {self.retry_policy.max}. "
                        f"Перезапуск браузера..."
                    )

                    await self.loader.close()
                    # await asyncio.sleep(5)
                    await self.loader.start()
                    continue

                await self.page_product_repository.add_products_bulk(slug=slug, items=entities)
                await self.processed_pages.add_url(slug=slug, page=page)

                paginator = paginator.mark_processed()
                yield entities
                await asyncio.sleep(5)

            logger.info(f"Scraping completed: {slug}")
            await self.loader.close()

        except CategoryNotFoundError:
            logger.warning(f"Category '{slug}' not found")
            await self.loader.close()
            raise

        except DatabaseOperationError:
            logger.error(f"Database error while processing slug='{slug}'")
            await self.loader.close()
            raise

        except DatabaseConnectionError:
            logger.error("The database is unavailable - I'll try again later.")
            await self.loader.close()
            raise

        except ValueObjectProductValidationError:
            logger.error("Validation error")
            await self.loader.close()
            raise
