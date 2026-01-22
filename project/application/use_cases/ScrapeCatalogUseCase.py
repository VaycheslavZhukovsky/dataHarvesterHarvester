from itertools import chain

from project.application.use_cases.scrape_all import scrape_all
from project.domain.exceptions.ProductError import ValueObjectProductValidationError
from project.infrastructure.exceptions.db_exceptions import CategoryNotFoundError, DatabaseOperationError, \
    DatabaseConnectionError
from project.infrastructure.exceptions.parsing_errors import ParsingError
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class MultipleSlugsError(Exception):
    pass


class ScrapeCatalogUseCase:
    def __init__(
            self,
            loader,
            extractor,
            mapper,
            processed_pages,
            first_page_load_category_uc,
            recovery_processed_data_category_uc,
            scraper_page_uc,
            url_parts,
            page_category_total_products,
            retry_policy,
            page_product_repository,
    ):
        self.loader = loader
        self.mapper = mapper
        self.extractor = extractor
        self.processed_pages = processed_pages
        self.url_parts = url_parts
        self.page_category_total_products = page_category_total_products
        self.retry_policy = retry_policy
        self.page_product_repository = page_product_repository
        self.first_page_load_category_uc = first_page_load_category_uc
        self.recovery_processed_data_category_uc = recovery_processed_data_category_uc

        self.scraper_page_uc = scraper_page_uc

    async def execute(self, url: str):

        NUMBER_OF_COMPETITIVE_PAGES = 5
        logger.info(f"Starting catalog scraping for URL: {url}")

        slug = self.url_parts.from_url(url).segments[1]

        try:
            all_pages, processed_pages = await self.processed_pages.get_loaded_pages(slug)


            paginator = self.recovery_processed_data_category_uc.assemble_paginator(url, all_pages, processed_pages)

            while True:
                urls = []
                pages = []
                slugs = []
                pages_and_slugs = {}
                for _ in range(NUMBER_OF_COMPETITIVE_PAGES):
                    if (url := paginator.next_url()) is None:
                        break
                    pages.append(paginator.current_page())
                    slugs.append(paginator.parts.segments[1])

                    paginator = paginator.mark_processed()
                    urls.append(url)

                for slug, page in zip(slugs, pages):
                    pages_and_slugs.setdefault(slug, []).append(page)

                if not urls:
                    break

                logger.debug(f"Scraping page: {urls}")
                logger.debug(f"Total page: {pages}")
                logger.debug(f"Total slug: {slugs}")
                logger.debug(f"Total pages_and_slugs: {pages_and_slugs}")

                try:

                    results = await scrape_all(urls, self.loader, self.extractor, self.mapper)
                    self.retry_policy.register_success()
                    results = list(chain.from_iterable(results.values()))

                    if len(set(slugs)) == 1:
                        await self.page_product_repository.add_products_bulk(slug=slugs[0], items=results)
                    else:
                        raise MultipleSlugsError(f"Ожидался один slug, но получено: {slugs}")

                    for slug, pages in pages_and_slugs.items():
                        for page in pages:
                            await self.processed_pages.add_url(slug=slug, page=page)

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

                yield results

            logger.info(f"Scraping completed: {slug}")

        except CategoryNotFoundError:
            logger.warning(f"Category '{slug}' not found")
            raise

        except DatabaseOperationError:
            logger.error(f"Database error while processing slug='{slug}'")
            raise

        except DatabaseConnectionError:
            logger.error("The database is unavailable - I'll try again later.")
            raise

        except ValueObjectProductValidationError:
            logger.error("Validation error")
            raise
