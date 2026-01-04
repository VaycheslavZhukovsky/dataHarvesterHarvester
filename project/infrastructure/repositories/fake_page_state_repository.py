from pathlib import Path
from typing import Tuple, List

from project.domain.repositories.IPageStateRepository import IPageStateRepository


class FakePageStateRepository(IPageStateRepository):
    """
    Файловая заглушка вместо БД.
    Хранит список обработанных URL в текстовом файле.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создаёт файл, если его нет."""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text("", encoding="utf-8")

    def _read_urls(self) -> List[str]:
        """Читает все URL из файла."""
        self._ensure_file_exists()
        content = self.file_path.read_text(encoding="utf-8").strip()
        if not content:
            return []
        return content.split("\n")

    def _write_urls(self, urls: List[str]):
        """Перезаписывает файл списком URL."""
        text = "\n".join(urls)
        self.file_path.write_text(text, encoding="utf-8")

    def add_url(self, url: str) -> None:
        """
        Добавляет URL в файл, если его там нет.
        """
        urls = self._read_urls()

        if url not in urls:
            urls.append(url)
            self._write_urls(urls)

    def get_data_from_category(self, url: str) -> Tuple[int, Tuple[int, ...]]:
        """
        Возвращает:
        - total_pages (заглушка)
        - tuple обработанных страниц (по URL)
        """

        urls = self._read_urls()

        # фильтруем только URL этой категории
        processed_pages = []

        for u in urls:
            if u.startswith(url):
                # извлекаем page=N
                if "page=" in u:
                    try:
                        page_num = int(u.split("page=")[1])
                        processed_pages.append(page_num)
                    except ValueError:
                        pass
                else:
                    # базовая страница = page 1
                    processed_pages.append(1)

        processed_pages = sorted(set(processed_pages))

        # total_pages — заглушка, позже заменишь на реальное значение
        total_pages = 5

        return total_pages, tuple(processed_pages)
