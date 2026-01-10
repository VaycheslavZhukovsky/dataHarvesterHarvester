from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode


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

    def with_page(self, page: int) -> "UrlParts":
        """Возвращает новый UrlParts с обновлённым параметром page."""
        if page < 1:
            raise ValueError("page must be >= 1")
        new_query = dict(self.query)
        new_query["page"] = str(page)
        return UrlParts(domain=self.domain, segments=self.segments, query=new_query)

    def to_url(self, scheme: str = "https") -> str:
        """Генерирует строку URL из частей."""
        return urlunparse((
            scheme,
            self.domain,
            "/" + "/".join(self.segments),
            "",
            urlencode(self.query),
            ""
        ))

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
