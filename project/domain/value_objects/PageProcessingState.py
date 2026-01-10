from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class PageProcessingState:
    """
    Value Object representing the pagination state.
    total_pages can be None until the first page is loaded.
    """
    total_pages: Optional[int] = None
    processed_pages: List[int] = field(default_factory=list)

    # ---------------------------
    # Установка total_pages
    # ---------------------------
    def with_total_pages(self, total_pages: int) -> "PageProcessingState":
        """
        Returns a new state with total_pages set.
        If total_pages is already set, changing it is not allowed.
        """
        if total_pages < 1:
            raise ValueError("total_pages must be >= 1")

        if self.total_pages is not None:
            raise ValueError("total_pages is already set and cannot be changed.")

        return PageProcessingState(
            total_pages=total_pages,
            processed_pages=self.processed_pages
        )

    # ---------------------------
    # Добавление обработанной страницы
    # ---------------------------
    def add_processed(self, page: int) -> "PageProcessingState":
        """
        Adds the processed page.
        If total_pages is not yet known, we only allow page >= 1.
        """
        if page < 1:
            raise ValueError("The page number must be greater than or equal to 1.")

        if self.total_pages is not None and page > self.total_pages:
            raise ValueError(
                f"Page {page} is outside the range {self.total_pages}"
            )

        new_pages = sorted(set(self.processed_pages + [page]))
        return PageProcessingState(
            total_pages=self.total_pages,
            processed_pages=new_pages
        )

    # ---------------------------
    # Текущая страница
    # ---------------------------
    def current_page(self) -> Optional[int]:
        """
        Returns the next page to process.
        If total_pages is unknown, return:
            1 if nothing has been processed yet
            max(processed_pages) + 1 if something has already been processed
        """
        if self.total_pages is None:
            if not self.processed_pages:
                return 1
            return max(self.processed_pages) + 1

        # total_pages известен
        for page in range(1, self.total_pages + 1):
            if page not in self.processed_pages:
                return page
        return None

    def is_finished(self) -> bool:
        if self.total_pages is None:
            return False

        return len(self.processed_pages) >= self.total_pages
