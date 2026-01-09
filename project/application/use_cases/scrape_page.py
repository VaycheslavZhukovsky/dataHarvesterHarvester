from project.infrastructure.exceptions.parsing_errors import ParsingError


class ScrapeAllProductsFromPageUseCase:
    def __init__(self, loader, product_extractor_from_html, mapper):
        self.loader = loader
        self.product_extractor_from_html = product_extractor_from_html
        self.mapper = mapper

    async def get_all_products(self, url: str):
        html = await self.loader.load_dom(url)

        try:
            products_raw = self.product_extractor_from_html.create_products_list_from_str(html)
        except ParsingError:
            raise ParsingError
        except Exception as e:
            raise RuntimeError(f"Failed to extract products on page {url}: {e}")

        return self.mapper.asemble_entities(products_raw)
