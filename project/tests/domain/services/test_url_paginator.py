from urllib.parse import urlparse, parse_qs

from project.domain.services.url_paginator import UrlPaginator
from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_state import PageProcessingState


def test_current_page_and_next_url():
    state = PageProcessingState(total_pages=3)
    url = "https://example.com/catalog/items"
    parts = UrlParts.from_url(url)
    paginator = UrlPaginator(parts=parts, state=state)

    assert paginator.current_page() == 1
    next_url = paginator.next_url()
    parsed = urlparse(next_url)
    query = parse_qs(parsed.query)
    assert query["page"] == ["1"]

    paginator = paginator.mark_processed()
    assert paginator.current_page() == 2

    next_url = paginator.next_url()
    parsed = urlparse(next_url)
    query = parse_qs(parsed.query)
    assert query["page"] == ["2"]


def test_mark_processed_creates_new_object():
    state = PageProcessingState(total_pages=2)
    url = "https://example.com/items"
    parts = UrlParts.from_url(url)
    paginator = UrlPaginator(parts=parts, state=state)

    paginator2 = paginator.mark_processed()
    assert paginator.current_page() == 1
    assert paginator2.current_page() == 2


def test_all_pages_processed_returns_none():
    state = PageProcessingState(total_pages=2)
    url = "https://example.com/items"
    parts = UrlParts.from_url(url)
    paginator = UrlPaginator(parts=parts, state=state)

    paginator = paginator.mark_processed().mark_processed()
    assert paginator.current_page() is None
    assert paginator.next_url() is None


def test_preserves_query_parameters():
    state = PageProcessingState(total_pages=2)
    url = "https://example.com/items?sort=asc"
    parts = UrlParts.from_url(url)
    paginator = UrlPaginator(parts=parts, state=state)

    next_url = paginator.next_url()
    parsed = urlparse(next_url)
    query = parse_qs(parsed.query)
    assert query["page"] == ["1"]
    assert query["sort"] == ["asc"]


def test_multiple_pages_processing_loop():
    state = PageProcessingState(total_pages=3)
    url = "https://example.com/items"
    parts = UrlParts.from_url(url)
    paginator = UrlPaginator(parts=parts, state=state)

    urls = []
    while paginator.current_page() is not None:
        urls.append(paginator.next_url())
        paginator = paginator.mark_processed()

    expected = [
        "https://example.com/items?page=1",
        "https://example.com/items?page=2",
        "https://example.com/items?page=3",
    ]
    assert urls == expected
