import hashlib
from pathlib import Path


class CacheIndex:
    """Индекс кеша: хранит md5-хэши файлов и позволяет проверять один URL."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self._hashes = self._load_hashes()

    def _load_hashes(self) -> set[str]:
        """Сканирует директорию и собирает все имена файлов без расширения."""
        return {
            file.stem
            for file in self.cache_dir.iterdir()
            if file.is_file() and file.suffix == ".html"
        }

    @staticmethod
    def _hash_url(url: str) -> str:
        return hashlib.md5(url.encode("utf-8")).hexdigest()

    def has_url(self, url: str) -> bool:
        """Возвращает True, если файл для данного URL существует."""
        return self._hash_url(url) in self._hashes
