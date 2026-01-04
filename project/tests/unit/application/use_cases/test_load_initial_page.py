import pytest
from unittest.mock import AsyncMock, MagicMock

from project.application.use_cases.load_init_page import LoadInitialPageUseCase


@pytest.mark.asyncio
async def test_load_initial_page_success():
    loader = AsyncMock()
    loader.load_dom.return_value = "<html>products: 90</html>"

    paginator = MagicMock()
    paginator_factory = MagicMock()
    paginator_factory.create.return_value = paginator

    uc = LoadInitialPageUseCase(loader, paginator_factory)

    result = await uc.execute("http://example.com")

    loader.load_dom.assert_called_once_with("http://example.com")
    paginator_factory.create.assert_called_once()
    assert result is paginator


@pytest.mark.asyncio
async def test_load_initial_page_minimum_one_page():
    loader = AsyncMock()
    loader.load_dom.return_value = "<html>products: 0</html>"

    paginator = MagicMock()
    paginator_factory = MagicMock()
    paginator_factory.create.return_value = paginator

    uc = LoadInitialPageUseCase(loader, paginator_factory)

    result = await uc.execute("http://example.com")

    assert result is paginator
