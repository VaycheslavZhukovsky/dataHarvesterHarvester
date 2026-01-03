from typing import Protocol, Tuple


class IPageStateRepository(Protocol):
    """
    Интерфейс репозитория, который знает,
    какие страницы по данному URL уже были загружены.
    """

    def get_data_from_category(self, url: str) -> Tuple[int, Tuple[int, ...]]:
        """Вернуть кортеж обработанных страниц."""
        raise NotImplementedError
