from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ScrapeCatalogUseCase:
    def __init__(
            self,
            loader,
            extractor,
            mapper,
            paginator_factory,
            page_state_service,
            load_initial_uc,
            restore_paginator_uc,
            scrape_page_uc,
    ):
        self.loader = loader
        self.extractor = extractor
        self.mapper = mapper
        self.paginator_factory = paginator_factory
        self.page_state_service = page_state_service

        self.load_initial_uc = load_initial_uc(loader, paginator_factory)
        self.restore_paginator_uc = restore_paginator_uc(paginator_factory)
        self.scrape_page_uc = scrape_page_uc

    async def execute(self, url: str):
        logger.info(f"Starting catalog scraping for URL: {url}")

        all_pages, processed = self.page_state_service.get_loaded_pages(url)

        await self.loader.start()

        if not processed:
            paginator = await self.load_initial_uc.execute(url)
        else:
            paginator = self.restore_paginator_uc.execute(url, all_pages, processed)

        while True:
            page_url = paginator.next_url()
            if not page_url:
                break

            logger.info(f"Scraping page: {page_url}")

            entities = await self.scrape_page_uc.execute(page_url)

            self.page_state_service.add_url(page_url)
            paginator = paginator.mark_processed()

            yield entities

        logger.info("Scraping completed")
