from project.infrastructure.exceptions.parsing_errors import ParsingError


class ScrapeSinglePageUseCase:
    def __init__(self, loader, extractor, mapper):
        self.loader = loader
        self.extractor = extractor
        self.mapper = mapper

    async def execute(self, url: str):
        html = await self.loader.load_dom(url)

        try:
            products_raw = self.extractor.create_products_list_from_str(html)
        except ParsingError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to extract products on page {url}: {e}")

        return self.mapper.to_entities(products_raw)
