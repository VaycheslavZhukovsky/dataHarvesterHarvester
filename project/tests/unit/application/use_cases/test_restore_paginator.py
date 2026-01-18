import pytest
from unittest.mock import MagicMock, AsyncMock

from project.application.use_cases.ScrapeAllProductsFromPageUseCase import ScrapeAllProductsFromPageUseCase
from project.infrastructure.exceptions.parsing_errors import ParsingError


@pytest.mark.asyncio
async def test_get_all_products_success():
    # Arrange
    loader = MagicMock()
    loader.load_dom = AsyncMock(return_value="<html>OK</html>")

    extractor = MagicMock()
    extractor.create_products_list_from_str.return_value = [{"id": 1}, {"id": 2}]

    mapper = MagicMock()
    mapper.asemble_entities.return_value = ["entity1", "entity2"]

    use_case = ScrapeAllProductsFromPageUseCase(loader, extractor, mapper)

    # Act
    result = await use_case.get_all_products("https://example.com")

    # Assert
    loader.load_dom.assert_awaited_once_with("https://example.com")
    extractor.create_products_list_from_str.assert_called_once_with("<html>OK</html>")
    mapper.asemble_entities.assert_called_once_with([{"id": 1}, {"id": 2}])

    assert result == ["entity1", "entity2"]


@pytest.mark.asyncio
async def test_get_all_products_parsing_error():
    loader = MagicMock()
    loader.load_dom = AsyncMock(return_value="<html>broken</html>")

    extractor = MagicMock()
    extractor.create_products_list_from_str.side_effect = ParsingError("bad html")

    mapper = MagicMock()

    use_case = ScrapeAllProductsFromPageUseCase(loader, extractor, mapper)

    with pytest.raises(ParsingError):
        await use_case.get_all_products("https://example.com")


@pytest.mark.asyncio
async def test_get_all_products_unexpected_error():
    loader = MagicMock()
    loader.load_dom = AsyncMock(return_value="<html>OK</html>")

    extractor = MagicMock()
    extractor.create_products_list_from_str.side_effect = ValueError("boom")

    mapper = MagicMock()

    use_case = ScrapeAllProductsFromPageUseCase(loader, extractor, mapper)

    with pytest.raises(RuntimeError) as exc:
        await use_case.get_all_products("https://example.com")

    assert "Failed to extract products on page https://example.com" in str(exc.value)
    assert "boom" in str(exc.value)
