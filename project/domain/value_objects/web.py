from urllib.parse import urlparse

from dataclasses import dataclass


@dataclass(frozen=True)
class HtmlContent:
    raw: str

    def __post_init__(self):
        if "<html" not in self.raw.lower():
            raise ValueError("Invalid HTML content")

    def length(self) -> int:
        return len(self.raw)

    def contains(self, text: str) -> bool:
        return text.lower() in self.raw.lower()


@dataclass(frozen=True)
class Url:
    value: str

    def __post_init__(self):
        parsed = urlparse(self.value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {self.value}")

    def domain(self) -> str:
        return urlparse(self.value).netloc
