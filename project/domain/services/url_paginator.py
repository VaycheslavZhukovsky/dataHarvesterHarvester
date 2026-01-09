from dataclasses import dataclass
from typing import Optional

from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_state import PageProcessingState


@dataclass(frozen=True)
class UrlPaginator:
    parts: UrlParts
    state: PageProcessingState
    total_products: Optional[int]

    def current_page(self) -> Optional[int]:
        """Возвращает текущую страницу для обработки или None, если всё обработано."""
        return self.state.current_page()

    def next_url(self) -> Optional[str]:
        """
        Возвращает URL следующей страницы и обновлённое состояние.
        Если все страницы обработаны — возвращает None.
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
        Возвращает новый UrlPaginator с обновлённым состоянием,
        где страница помечена как обработанная.
        Если page не указан — используется текущая.
        """
        if page is None:
            page = self.current_page()
        if page is None:
            return self

        new_state = self.state.add_processed(page)
        return UrlPaginator(parts=self.parts, state=new_state, total_products=self.total_products)
