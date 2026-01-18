from dataclasses import dataclass
from typing import Optional

from project.domain.value_objects.UrlParts import UrlParts
from project.domain.value_objects.PageProcessingState import PageProcessingState


@dataclass(frozen=True)
class UrlPaginator:
    parts: UrlParts
    state: PageProcessingState
    total_products: Optional[int]

    def current_page(self) -> Optional[int]:
        """Returns the current page for processing, or None if all pages have been processed."""
        return self.state.current_page()

    def next_url(self) -> Optional[str]:
        """
        Returns the URL of the next page and the updated state.
        If all pages have been processed, it returns None.
        """
        page = self.state.current_page()
        if page is None:
            return None

        new_query = dict(self.parts.query)
        new_query["page"] = str(page)

        url = self.parts.with_page(page)
        return url.to_url()

    def mark_processed(self, page: Optional[int] = None) -> "UrlPaginator":
        """
        Returns a new UrlPaginator with updated state,
        where the page is marked as processed.
        If page is not specified, the current page is used.
        """
        if page is None:
            page = self.current_page()
        if page is None:
            return UrlPaginator(
                parts=self.parts,
                state=self.state,
                total_products=self.total_products,
            )

        new_state = self.state.add_processed(page)
        return UrlPaginator(parts=self.parts, state=new_state, total_products=self.total_products)


def mark_processed(self, page: Optional[int] = None) -> "UrlPaginator":
    if page is None:
        page = self.current_page()

    # finished — но возвращаем новый объект, чтобы сохранить immutability
    if page is None:
        return UrlPaginator(
            parts=self.parts,
            state=self.state,
            total_products=self.total_products,
        )

    new_state = self.state.add_processed(page)
    return UrlPaginator(parts=self.parts, state=new_state, total_products=self.total_products)
