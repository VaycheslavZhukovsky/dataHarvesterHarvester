import pytest
from unittest.mock import AsyncMock, MagicMock

from project.application.use_cases.scrape_single_page import ScrapeSinglePageUseCase
from project.infrastructure.exceptions.parsing_errors import ParsingError


@pytest.mark.asyncio
async def test_scrape_single_page_success():
    loader = AsyncMock()
    loader.load_dom.return_value = "<html>ok</html>"

    extractor = MagicMock()
    extractor.create_products_list_from_str.return_value = [{"id": 1}]

    mapper = MagicMock()
    mapper.to_entities.return_value = ["entity1"]

    uc = ScrapeSinglePageUseCase(loader, extractor, mapper)

    result = await uc.execute("http://example.com")

    loader.load_dom.assert_called_once()
    extractor.create_products_list_from_str.assert_called_once()
    mapper.to_entities.assert_called_once()

    assert result == ["entity1"]


@pytest.mark.asyncio
async def test_scrape_single_page_parsing_error():
    loader = AsyncMock()
    loader.load_dom.return_value = "<html>bad</html>"

    extractor = MagicMock()
    extractor.create_products_list_from_str.side_effect = ParsingError("bad")

    mapper = MagicMock()

    uc = ScrapeSinglePageUseCase(loader, extractor, mapper)

    with pytest.raises(ParsingError):
        await uc.execute("http://example.com")


@pytest.mark.asyncio
async def test_scrape_single_page_unexpected_error():
    loader = AsyncMock()
    loader.load_dom.return_value = "<html>bad</html>"

    extractor = MagicMock()
    extractor.create_products_list_from_str.side_effect = Exception("boom")

    mapper = MagicMock()

    uc = ScrapeSinglePageUseCase(loader, extractor, mapper)

    with pytest.raises(RuntimeError):
        await uc.execute("http://example.com")
