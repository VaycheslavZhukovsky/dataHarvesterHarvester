from pathlib import Path

from project.infrastructure.cache_index import CacheIndex
from project.config import SUBCATEGORIES
from project.infrastructure.factories.paginator_factory import PaginatorFactory

root = Path(__file__).resolve().parent

path_cache = root / "infrastructure" / "cache"
cache = CacheIndex(Path(path_cache))
# url = "https://lemanapro.ru/catalogue/dekor-po-stilyam/"

for subcategory in SUBCATEGORIES:
    url = f"https://lemanapro.ru/catalogue/{subcategory}"

    paginator = PaginatorFactory.create(url, 10)
    page_url = paginator.next_url()
    paginator = paginator.mark_processed()
    new_url = paginator.next_url()
    while True:
        if cache.has_url(url):
            print(f"Есть в кеше: {cache.has_url(url)} - {url}")

        url = paginator.next_url()
        paginator = paginator.mark_processed()
        # print(f"Есть в кеше: {cache.has_url(url)} - {url}")

