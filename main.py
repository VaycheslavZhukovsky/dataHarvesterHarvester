import asyncio

from project.application.ScraperApp import ScraperApp
from project.application.bootstrap.InitialDataLoader import InitialDataLoader
from project.config import SUBCATEGORIES
from project.domain.exceptions.ProductError import ValueObjectProductValidationError
from project.infrastructure.exceptions.db_exceptions import DatabaseError
from project.infrastructure.exceptions.parsing_errors import ParsingError
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)

LIMIT_PAGES = 5


async def main():
    try:
        # loader = InitialDataLoader()
        # await loader.run(limit_pages=LIMIT_PAGES)

        app = ScraperApp()
        await app.scrape_category(category_slug=SUBCATEGORIES[0], limit_pages=LIMIT_PAGES)

    except ParsingError:
        logger.error("Parsing error.")

    except DatabaseError:
        logger.error(f"Database error while processing slug='{SUBCATEGORIES[0]}'")
        raise

    except ValueObjectProductValidationError:
        logger.error("Validation error")
        raise


if __name__ == "__main__":
    asyncio.run(main())
