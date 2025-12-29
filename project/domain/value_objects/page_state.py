from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class PageProcessingState:
    """Value Object состояния пагинации."""
    total_pages: int
    processed_pages: List[int] = field(default_factory=list)

    def add_processed(self, page: int) -> "PageProcessingState":
        """
        Возвращает новый объект с добавленной обработанной страницей.
        Страницы уникальны и не дублируются.
        """
        if page < 1 or page > self.total_pages:
            raise ValueError(f"Страница {page} вне диапазона 1..{self.total_pages}")

        # создаём новое состояние (immutable подход)
        new_pages = sorted(set(self.processed_pages + [page]))
        return PageProcessingState(
            total_pages=self.total_pages,
            processed_pages=new_pages
        )

    def current_page(self) -> Optional[int]:
        """
        Возвращает следующую страницу для обработки или None, если всё обработано.
        """
        for page in range(1, self.total_pages + 1):
            if page not in self.processed_pages:
                return page
        return None  # все страницы обработаны

    def is_finished(self) -> bool:
        """True - если все страницы обработаны."""
        return len(self.processed_pages) >= self.total_pages
