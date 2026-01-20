import asyncio

from project.application.ScraperApp import ScraperApp
from project.application.bootstrap.InitialDataLoader import InitialDataLoader
from project.config import SUBCATEGORIES


async def main():
    loader = InitialDataLoader()
    await loader.run()

    app = ScraperApp()
    await app.scrape_category(SUBCATEGORIES[0])


if __name__ == "__main__":
    asyncio.run(main())
