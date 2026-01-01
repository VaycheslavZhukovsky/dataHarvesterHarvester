import pytest

from project.tests.unit.factories.mock_page_loader import MockPageLoader


@pytest.mark.asyncio
async def test_page_fetcher_uses_loader():
    loader = MockPageLoader("<body>OK</body>")

    html = await loader.load_dom("https://example.com")

    assert html == "<body>OK</body>"
    assert loader.loaded_urls == ["https://example.com"]
