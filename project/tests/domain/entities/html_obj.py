
from project.domain.entities.html_obj import WebPage
from project.domain.value_objects.html_obj import HtmlContent, UrlParts


def test_webpage_creation():
    url = "https://example.com/list?page=1&sort=asc"
    html = "<html>" + "a" * 2001 + "</html>"

    parts = UrlParts.from_url(url)
    content = HtmlContent(html=html)

    page = WebPage(url=parts, html=content)

    assert page.url == parts
    assert page.html == content
    assert page.html.html.startswith("<html>")

