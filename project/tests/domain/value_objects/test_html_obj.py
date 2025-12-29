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
def test_basic_url():
    url = "https://example.com"
    parts = UrlParts.from_url(url)
    assert parts.domain == "example.com"
    assert parts.segments == ()
    assert parts.query == {}
    assert str(parts) == "https://example.com/"


def test_url_with_segments():
    url = "https://example.com/foo/bar/"
    parts = UrlParts.from_url(url)
    assert parts.domain == "example.com"
    assert parts.segments == ("foo", "bar")
    assert parts.query == {}
    assert str(parts) == "https://example.com/foo/bar"


def test_url_with_query():
    url = "https://example.com/search?q=test&lang=en"
    parts = UrlParts.from_url(url)
    assert parts.domain == "example.com"
    assert parts.segments == ("search",)
    assert parts.query == {"q": "test", "lang": "en"}
    assert str(parts) == "https://example.com/search/?q=test&lang=en"


def test_page_parameter_removal():
    url = "https://example.com/list?page=1&sort=asc"
    parts = UrlParts.from_url(url)
    assert parts.query == {"sort": "asc"}
    assert "page" not in parts.query


def test_page_parameter_validation():
    url = "https://example.com/list?page=0"
    with pytest.raises(ValueError, match="page must be > 0"):
        UrlParts.from_url(url)


def test_invalid_url_no_domain():
    url = "https:///path"
    with pytest.raises(ValueError, match="URL must contain a domain"):
        UrlParts.from_url(url)
