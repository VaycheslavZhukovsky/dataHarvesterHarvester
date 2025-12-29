from dataclasses import dataclass

from project.domain.value_objects.html_obj import UrlParts, HtmlContent


@dataclass
class WebPage:
    url: UrlParts
    html: HtmlContent
