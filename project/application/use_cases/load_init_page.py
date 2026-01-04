from project.domain.services.number_of_products_extractor import get_number_of_products


class LoadInitialPageUseCase:
    def __init__(self, loader, paginator_factory):
        self.loader = loader
        self.paginator_factory = paginator_factory

    async def execute(self, url: str):
        html = await self.loader.load_dom(url)
        total_products = get_number_of_products(html)
        total_pages = max(1, total_products // 30)

        paginator = self.paginator_factory.create(url, total_pages)
        return paginator
