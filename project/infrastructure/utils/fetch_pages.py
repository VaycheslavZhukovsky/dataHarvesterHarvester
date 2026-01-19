import asyncio

from project.infrastructure.exceptions.parsing_errors import ParsingError
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


async def fetch_pages(urls, loader, html_queue):
    for url in urls:
        while True:
            html = await loader.load_dom(url)
            await html_queue.put((url, html))
            break  # успех — идём к следующему URL


def parse_and_map(html, extractor, mapper):
    # если create_products_list_from_str выбросит JsonBlockNotFoundError,
    # исключение поднимется в event loop
    products_raw = extractor.create_products_list_from_str(html)
    return mapper.asemble_entities(products_raw)


async def cpu_worker(html_queue, extractor, mapper, executor, results, error_queue):
    loop = asyncio.get_running_loop()

    while True:
        item = await html_queue.get()
        if item is None:
            break

        url, html = item

        try:
            entities = await loop.run_in_executor(
                executor,
                parse_and_map,
                html,
                extractor,
                mapper
            )
        except ParsingError as e:
            await error_queue.put((url, e))
            continue
        except Exception as e:
            await error_queue.put((url, RuntimeError(f"Unexpected error: {e}")))
            raise

        results[url] = entities


async def error_handler(error_queue, total_urls: int):
    errors_batch = 0

    while True:
        url, err = await error_queue.get()

        # сигнал завершения
        if err is None:
            break

        errors_batch += 1
        logger.error(f"Parsing error on {url}: {err}. Errors in batch: {errors_batch}")

        # если ошибок столько же, сколько URL — весь батч упал
        if errors_batch == total_urls:

            logger.warning(
                f"All {total_urls} pages failed parsing. "
            )

            # после регистрации ошибки — пробрасываем исключение
            raise ParsingError(
                f"All {total_urls} pages failed parsing. "
            )
