import asyncio

import pytest
from unittest.mock import AsyncMock, MagicMock

from project.application.use_cases.ScrapeCatalogUseCase import ScrapeCatalogUseCase
from project.infrastructure.exceptions.parsing_errors import ParsingError
from project.infrastructure.exceptions.db_exceptions import (
    CategoryNotFoundError,
    DatabaseOperationError,
    DatabaseConnectionError,
)
from project.domain.exceptions.ProductError import ValueObjectProductValidationError

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch):
    async def fake_sleep(*args, **kwargs):
        return None

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)


@pytest.fixture
def use_case():
    loader = AsyncMock()
    processed_pages = AsyncMock()
    first_page_uc = AsyncMock()
    recovery_uc = MagicMock()
    scraper_page_uc = AsyncMock()
    url_parts = MagicMock()
    page_category_total_products = AsyncMock()
    page_product_repository = AsyncMock()
    retry_policy = MagicMock()

    url_parts.from_url.return_value.segments = ["catalogue", "oboi-pod-pokrasku"]

    uc = ScrapeCatalogUseCase(
        loader=loader,
        processed_pages=processed_pages,
        first_page_load_category_uc=first_page_uc,
        recovery_processed_data_category_uc=recovery_uc,
        scraper_page_uc=scraper_page_uc,
        url_parts=url_parts,
        page_category_total_products=page_category_total_products,
        page_product_repository=page_product_repository,
        retry_policy=retry_policy,
    )

    return {
        "uc": uc,
        "loader": loader,
        "processed_pages": processed_pages,
        "first_page_uc": first_page_uc,
        "recovery_uc": recovery_uc,
        "scraper_page_uc": scraper_page_uc,
        "url_parts": url_parts,
        "page_category_total_products": page_category_total_products,
        "page_product_repository": page_product_repository,
        "retry_policy": retry_policy,
    }


# ---------------------------------------------------------
# CASE 1: первая загрузка
# ---------------------------------------------------------
async def test_execute_first_page_flow(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.return_value = ([], [])

    paginator = MagicMock()
    paginator.total_products = 100
    paginator.parts.segments = ["catalogue", "oboi"]
    paginator.next_url.side_effect = ["url1", None]
    paginator.current_page.return_value = 1
    paginator.mark_processed.return_value = paginator

    use_case["first_page_uc"].get_total_products.return_value = paginator
    use_case["scraper_page_uc"].get_all_products.return_value = ["p1", "p2"]

    results = []
    async for entities in uc.execute("https://site/catalogue/oboi/"):
        results.append(entities)

    assert results == [["p1", "p2"]]
    use_case["loader"].start.assert_called_once()
    use_case["loader"].close.assert_called_once()


# ---------------------------------------------------------
# CASE 2: восстановление
# ---------------------------------------------------------
async def test_execute_recovery_flow(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.return_value = ([1, 2], [1])

    paginator = MagicMock()
    paginator.next_url.side_effect = ["url2", None]
    paginator.current_page.return_value = 2
    paginator.parts.segments = ["catalogue", "oboi"]
    paginator.mark_processed.return_value = paginator

    use_case["recovery_uc"].assemble_paginator.return_value = paginator
    use_case["scraper_page_uc"].get_all_products.return_value = ["x"]

    results = []
    async for entities in uc.execute("https://site/catalogue/oboi/"):
        results.append(entities)

    assert results == [["x"]]
    use_case["recovery_uc"].assemble_paginator.assert_called_once()


# ---------------------------------------------------------
# CASE 3: ParsingError → retry → success
# ---------------------------------------------------------
async def test_execute_parsing_retry_success(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.return_value = ([], [])

    paginator = MagicMock()
    paginator.total_products = 10
    paginator.parts.segments = ["catalogue", "oboi"]
    paginator.current_page.return_value = 1
    paginator.next_url.side_effect = ["url1", "url1", None]
    paginator.mark_processed.return_value = paginator

    use_case["first_page_uc"].get_total_products.return_value = paginator

    use_case["scraper_page_uc"].get_all_products.side_effect = [
        ParsingError("bad html"),
        ["ok"],
    ]

    use_case["retry_policy"].should_retry.side_effect = [True, False]
    use_case["retry_policy"].current = 0
    use_case["retry_policy"].max = 1

    results = []
    async for entities in uc.execute("https://site/catalogue/oboi/"):
        results.append(entities)

    assert results == [["ok"]]
    assert use_case["retry_policy"].register_failure.called
    assert use_case["retry_policy"].register_success.called


# ---------------------------------------------------------
# CASE 4: ParsingError → retry exhausted → проброс исключения
# ---------------------------------------------------------
async def test_execute_parsing_retry_exhausted(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.return_value = ([], [])

    paginator = MagicMock()
    paginator.total_products = 10
    paginator.parts.segments = ["catalogue", "oboi"]
    paginator.current_page.return_value = 1
    paginator.next_url.side_effect = ["url1"]
    use_case["first_page_uc"].get_total_products.return_value = paginator

    use_case["scraper_page_uc"].get_all_products.side_effect = ParsingError("bad html")

    use_case["retry_policy"].should_retry.return_value = False

    with pytest.raises(ParsingError):
        async for _ in uc.execute("https://site/catalogue/oboi/"):
            pass

    use_case["loader"].close.assert_called()


# ---------------------------------------------------------
# CASE 5: CategoryNotFoundError
# ---------------------------------------------------------
async def test_execute_category_not_found(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.side_effect = CategoryNotFoundError()

    with pytest.raises(CategoryNotFoundError):
        async for _ in uc.execute("url"):
            pass

    use_case["loader"].close.assert_called()


# ---------------------------------------------------------
# CASE 6: DatabaseOperationError
# ---------------------------------------------------------
async def test_execute_db_operation_error(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.side_effect = DatabaseOperationError()

    with pytest.raises(DatabaseOperationError):
        async for _ in uc.execute("url"):
            pass

    use_case["loader"].close.assert_called()


# ---------------------------------------------------------
# CASE 7: DatabaseConnectionError
# ---------------------------------------------------------
async def test_execute_db_connection_error(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.side_effect = DatabaseConnectionError()

    with pytest.raises(DatabaseConnectionError):
        async for _ in uc.execute("url"):
            pass

    use_case["loader"].close.assert_called()


# ---------------------------------------------------------
# CASE 8: ValueObjectProductValidationError
# ---------------------------------------------------------
async def test_execute_value_object_validation_error(use_case):
    uc = use_case["uc"]

    use_case["processed_pages"].get_loaded_pages.side_effect = ValueObjectProductValidationError()

    with pytest.raises(ValueObjectProductValidationError):
        async for _ in uc.execute("url"):
            pass

    use_case["loader"].close.assert_called()
