
from project.domain.services.page_type_detector import PageTypeDetector
from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_type import PageType

parts = UrlParts.from_url(url)
detector = PageTypeDetector(CATEGORIES, SUBCATEGORIES)

page_type = detector.detect(parts)

match page_type:
    case PageType.CATEGORY:
        ...
    case PageType.SUBCATEGORY:
        ...
    case PageType.PRODUCT:
        ...
