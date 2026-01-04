from functools import reduce


class RestorePaginatorUseCase:
    def __init__(self, paginator_factory):
        self.paginator_factory = paginator_factory

    def execute(self, url: str, all_pages: int, processed: list[int]):
        paginator = self.paginator_factory.create(url, all_pages)
        paginator = reduce(lambda acc, i: acc.mark_processed(i), processed, paginator)
        return paginator
