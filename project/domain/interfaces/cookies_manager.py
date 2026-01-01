from typing import Protocol


class ICookieProvider(Protocol):
    def build(self) -> list:
        pass



