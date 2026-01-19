import asyncio
from concurrent.futures.process import ProcessPoolExecutor

from project.infrastructure.utils.fetch_pages import fetch_pages, cpu_worker, error_handler


async def scrape_all(urls, loader, extractor, mapper):
    html_queue = asyncio.Queue()
    error_queue = asyncio.Queue()
    results = {}

    total_urls = len(urls)

    executor = ProcessPoolExecutor(max_workers=5)

    fetcher = asyncio.create_task(fetch_pages(urls, loader, html_queue))

    err_task = asyncio.create_task(
        error_handler(error_queue, total_urls)
    )

    workers = [
        asyncio.create_task(cpu_worker(html_queue, extractor, mapper, executor, results, error_queue))
        for _ in range(5)
    ]

    await fetcher

    for _ in range(len(workers)):
        await html_queue.put(None)

    await asyncio.gather(*workers)

    await error_queue.put((None, None))
    await err_task

    return results
