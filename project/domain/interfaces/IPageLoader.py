from typing import Protocol, Optional


class IPageLoader(Protocol):
    async def start(self) -> None:
        ...

    async def load_dom(self, url: str, timeout: Optional[int]):
        """Возвращает HTML как str"""
        ...

    async def close(self) -> None:
        ...
