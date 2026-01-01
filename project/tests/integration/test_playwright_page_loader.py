import pytest
from project.infrastructure.playwright.playwright_page_loader import PlaywrightPageLoader


@pytest.mark.asyncio
async def test_playwright_page_loader_integration():
    loader = PlaywrightPageLoader(
        proxy=None,
        cookies=[]
    )

    await loader.start()
    assert loader._pw is not None
    assert loader._context is not None

    html = await loader.load_dom("https://example.com")

    assert "<html" in html.lower()
    assert "example" in html.lower()

    await loader.close()

    assert loader._context is None
    assert loader._pw is None
