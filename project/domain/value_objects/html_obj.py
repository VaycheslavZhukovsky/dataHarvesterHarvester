from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs


from pydantic import BaseModel, field_validator


class HtmlContent(BaseModel):
    html: str
    min_chars: int = 2000

    model_config = {
        "frozen": True,
        "strict": True,
    }

    @field_validator('html')
    def check_length(cls, v, values):
        min_chars = values.data.get('min_chars', 2000)
        if len(v) <= min_chars:
            raise ValueError(f"HTML content must be longer than {min_chars} characters")
        return v

    def get_length(self) -> int:
        """Вернуть текущую длину документа."""
        return len(self.html)


@dataclass(frozen=True)
class UrlParts:
    domain: str
    segments: tuple[str, ...]
    query: dict[str, str]

    @classmethod
    def from_url(cls, url: str) -> "UrlParts":
        parsed = urlparse(url)

        domain = parsed.netloc
        if not domain:
            raise ValueError("URL must contain a domain")

        segments = tuple(
            segment for segment in parsed.path.split("/") if segment
        )

        raw_query = parse_qs(parsed.query)
        query = {k: v[0] for k, v in raw_query.items()}

        if "page" in query:
            page = int(query["page"])

            if page <= 0:
                raise ValueError("page must be > 0")

            if page == 1:
                del query["page"]

        return cls(
            domain=domain,
            segments=segments,
            query=query
        )

    def __str__(self):
        scheme = "https://"
        path = "/".join(self.segments)

        if self.query:
            query_string = "/?" + "&".join(f"{k}={v}" for k, v in self.query.items())
        else:
            query_string = ""

        return f"{scheme}{self.domain}/{path}{query_string}"


if __name__ == '__main__':
    url = "https://lemanapro.ru/catalogue/sad/?page=5"

    parts = UrlParts.from_url(url)

    print(parts.domain)
    print(parts.segments)
    print(parts.query)
    print(parts)
