from urllib.parse import urlparse, parse_qs

import pytest

from project.domain.value_objects.html_obj import HtmlContent, UrlParts


# -----------------------------
# HtmlContent
# -----------------------------
def test_create_valid_html_content():
    html = "<html>" + "a" * 2001 + "</html>"
    content = HtmlContent(html=html)
    assert content.get_length() == len(html)


def test_create_invalid_html_content():
    html = "<html>" + "a" * 1000 + "</html>"
    with pytest.raises(ValueError):
        HtmlContent(html=html)


def test_immutable_html_content():
    html = "<html>" + "a" * 2001 + "</html>"
    content = HtmlContent(html=html)
    with pytest.raises(ValueError):
        content.html = "<html>new content</html>"


# -----------------------------
# UrlParts
# -----------------------------
def test_from_url_basic():
    url = "https://example.com/catalog/items?sort=asc"
    parts = UrlParts.from_url(url)
    assert parts.domain == "example.com"
    assert parts.segments == ("catalog", "items")
    assert parts.query == {"sort": "asc"}


def test_from_url_with_page_1_removed():
    url = "https://example.com/catalog/items?page=1&sort=asc"
    parts = UrlParts.from_url(url)
    assert "page" not in parts.query
    assert parts.query == {"sort": "asc"}


def test_from_url_with_invalid_page_raises():
    with pytest.raises(ValueError):
        UrlParts.from_url("https://example.com/items?page=0")


def test_with_page_sets_page_param():
    url = "https://example.com/items?sort=asc"
    parts = UrlParts.from_url(url)
    parts2 = parts.with_page(2)

    # исходный объект не изменился
    assert parts.query == {"sort": "asc"}
    # новый объект имеет page
    assert parts2.query == {"sort": "asc", "page": "2"}


def test_with_page_invalid_raises():
    parts = UrlParts(domain="example.com", segments=("items",), query={})
    with pytest.raises(ValueError):
        parts.with_page(0)


def test_to_url_generates_correct_url():
    parts = UrlParts(domain="example.com", segments=("catalog", "items"), query={"sort": "asc", "page": "2"})
    url = parts.to_url()
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/catalog/items"
    assert query == {"sort": ["asc"], "page": ["2"]}


def test_str_method_without_query():
    parts = UrlParts(domain="example.com", segments=("catalog", "items"), query={})
    s = str(parts)
    assert s == "https://example.com/catalog/items"


def test_str_method_with_query():
    parts = UrlParts(domain="example.com", segments=("catalog", "items"), query={"sort": "asc", "page": "2"})
    s = str(parts)
    # query может быть в любом порядке, проверим наличие ключей и значений
    assert "https://example.com/catalog/items" in s
    assert "sort=asc" in s
    assert "page=2" in s


def test_multiple_segments_and_page():
    url = "https://example.com/a/b/c?page=3"
    parts = UrlParts.from_url(url)
    # page=3 должен остаться, так как >1
    assert parts.query.get("page") == "3"
    assert parts.segments == ("a", "b", "c")
