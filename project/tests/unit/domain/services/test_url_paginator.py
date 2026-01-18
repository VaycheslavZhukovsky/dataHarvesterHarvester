import pytest

from project.domain.services.UrlPaginator import UrlPaginator
from project.domain.value_objects.UrlParts import UrlParts
from project.domain.value_objects.PageProcessingState import PageProcessingState


@pytest.fixture
def parts():
    return UrlParts.from_url("https://example.com/catalog/?color=red")


@pytest.fixture
def state():
    return PageProcessingState(total_pages=3, processed_pages=[])


@pytest.fixture
def paginator(parts, state):
    return UrlPaginator(parts=parts, state=state, total_products=None)


# -----------------------------
# current_page()
# -----------------------------
def test_current_page_initial(paginator):
    assert paginator.current_page() == 1


def test_current_page_after_processing(parts):
    state = PageProcessingState(total_pages=3, processed_pages=[1, 2])
    paginator = UrlPaginator(parts=parts, state=state, total_products=None)

    assert paginator.current_page() == 3


def test_current_page_finished(parts):
    state = PageProcessingState(total_pages=2, processed_pages=[1, 2])
    paginator = UrlPaginator(parts=parts, state=state, total_products=None)

    assert paginator.current_page() is None


# -----------------------------
# next_url()
# -----------------------------
def test_next_url_first_page(paginator):
    url = paginator.next_url()
    assert url == "https://example.com/catalog?color=red&page=1"


def test_next_url_none_when_finished(parts):
    state = PageProcessingState(total_pages=2, processed_pages=[1, 2])
    paginator = UrlPaginator(parts=parts, state=state, total_products=None)

    assert paginator.next_url() is None


# -----------------------------
# mark_processed()
# -----------------------------
def test_mark_processed_implicit(paginator):
    """`mark_processed()` without an argument should mark the current page."""
    new_paginator = paginator.mark_processed()

    assert new_paginator.state.processed_pages == [1]
    assert paginator.state.processed_pages == []  # immutability


def test_mark_processed_explicit(parts, state):
    paginator = UrlPaginator(parts=parts, state=state, total_products=None)
    new_paginator = paginator.mark_processed(2)

    assert new_paginator.state.processed_pages == [2]
    assert paginator.state.processed_pages == []


def test_mark_processed_when_finished(parts):
    state = PageProcessingState(total_pages=1, processed_pages=[1])
    paginator = UrlPaginator(parts=parts, state=state, total_products=None)

    new_paginator = paginator.mark_processed()

    # ничего не меняется
    assert new_paginator.state.processed_pages == [1]
    assert new_paginator is not paginator  # but the object is new (immutable)


# -----------------------------
# next_url() + mark_processed() flow
# -----------------------------
def test_full_pagination_flow(parts):
    state = PageProcessingState(total_pages=3, processed_pages=[])
    paginator = UrlPaginator(parts=parts, state=state, total_products=None)

    urls = []
    while True:
        url = paginator.next_url()
        if url is None:
            break
        urls.append(url)
        paginator = paginator.mark_processed()

    assert urls == [
        "https://example.com/catalog?color=red&page=1",
        "https://example.com/catalog?color=red&page=2",
        "https://example.com/catalog?color=red&page=3",
    ]
