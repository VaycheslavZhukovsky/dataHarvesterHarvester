import pytest
from unittest.mock import AsyncMock, MagicMock

from project.application.use_cases.scrape_catalog_use_case import ScrapeCatalogUseCase


@pytest.mark.asyncio
async def test_scrape_catalog_full_flow():
    loader = AsyncMock()
    loader.start = AsyncMock()

    extractor = MagicMock()
    mapper = MagicMock()
    paginator_factory = MagicMock()

    page_state_service = MagicMock()
    page_state_service.get_loaded_pages.return_value = (5, [])

    # --- load_initial_uc ---
    paginator = MagicMock()
    paginator.next_url.side_effect = ["url1", "url2", None]
    paginator.mark_processed.side_effect = lambda: paginator

    load_initial_uc = MagicMock()
    load_initial_uc.return_value = MagicMock(execute=AsyncMock(return_value=paginator))

    restore_paginator_uc = MagicMock()

    scrape_page_uc = MagicMock()
    scrape_page_uc.execute = AsyncMock(side_effect=[["e1"], ["e2"]])

    uc = ScrapeCatalogUseCase(
        loader=loader,
        extractor=extractor,
        mapper=mapper,
        paginator_factory=paginator_factory,
        page_state_service=page_state_service,
        first_page_load_category_uc=lambda *a: load_initial_uc.return_value,
        recovery_processed_data_category_uc=lambda *a: restore_paginator_uc,
        scraper_page_uc=scrape_page_uc,
    )

    results = []
    async for batch in uc.execute("http://example.com"):
        results.append(batch)

    assert results == [["e1"], ["e2"]]

    loader.start.assert_called_once()
    assert scrape_page_uc.execute.await_count == 2
    assert page_state_service.add_url.call_count == 2
