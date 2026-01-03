from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class PageProcessingState:
    """
    Value Object состояния пагинации.
    total_pages может быть None до первой загрузки страницы.
    """
    total_pages: Optional[int] = None
    processed_pages: List[int] = field(default_factory=list)

    # ---------------------------
    # Установка total_pages
    # ---------------------------
    def with_total_pages(self, total_pages: int) -> "PageProcessingState":
        """
        Возвращает новое состояние с установленным total_pages.
        Если total_pages уже установлен — запрещаем менять.
        """
        if total_pages < 1:
            raise ValueError("total_pages должен быть >= 1")

        if self.total_pages is not None:
            raise ValueError("total_pages уже установлен и не может быть изменён")

        return PageProcessingState(
            total_pages=total_pages,
            processed_pages=self.processed_pages
        )

    # ---------------------------
    # Добавление обработанной страницы
    # ---------------------------
    def add_processed(self, page: int) -> "PageProcessingState":
        """
        Добавляет обработанную страницу.
        Если total_pages ещё неизвестен — разрешаем только page >= 1.
        """
        if page < 1:
            raise ValueError("Номер страницы должен быть >= 1")

        if self.total_pages is not None and page > self.total_pages:
            raise ValueError(
                f"Страница {page} вне диапазона 1..{self.total_pages}"
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
        Возвращает следующую страницу для обработки.
        Если total_pages неизвестен — возвращаем:
            1, если ничего не обработано
            max(processed_pages) + 1, если уже что-то обработано
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

    # ---------------------------
    # Завершена ли пагинация
    # ---------------------------
    def is_finished(self) -> bool:
        """
        Если total_pages неизвестен — пагинация не может быть завершена.
        """
        if self.total_pages is None:
            return False

        return len(self.processed_pages) >= self.total_pages
