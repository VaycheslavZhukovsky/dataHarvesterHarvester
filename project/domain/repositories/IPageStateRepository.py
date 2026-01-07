from typing import Protocol, Tuple


class IPageStateRepository(Protocol):
    """
    Интерфейс репозитория, который знает,
    какие страницы по данному URL уже были загружены.
    """
    async def add_url(self, slug: str, page: int) -> None:
        pass

    def get_data_from_category(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        """Вернуть кортеж обработанных страниц."""
        raise NotImplementedError
