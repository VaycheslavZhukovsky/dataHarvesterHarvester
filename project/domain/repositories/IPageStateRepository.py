from typing import Protocol, Tuple


class IPageStateRepository(Protocol):
    """
    A repository interface that knows
    which pages for a given URL have already been downloaded.
    """
    async def add_url(self, slug: str, page: int) -> None:
        pass

    def get_data_from_category(self, slug: str) -> Tuple[int, Tuple[int, ...]]:
        """Return a tuple of processed pages."""
        raise NotImplementedError
