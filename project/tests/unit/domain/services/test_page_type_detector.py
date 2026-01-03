from project.domain.services.page_type_detector import PageTypeDetector
from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_type import PageType

CATEGORIES = {"elki-novogodnie", "okna"}
SUBCATEGORIES = {"plastikovye", "derevyannye"}

detector = PageTypeDetector(CATEGORIES, SUBCATEGORIES)


def test_detect_category():
    parts = UrlParts.from_url("https://site.com/catalogue/elki-novogodnie/")
    assert detector.detect(parts) == PageType.CATEGORY


def test_detect_subcategory():
    parts = UrlParts.from_url("https://site.com/catalogue/plastikovye/")
    assert detector.detect(parts) == PageType.SUBCATEGORY


def test_detect_product():
    parts = UrlParts.from_url("https://site.com/product/sku123/")
    assert detector.detect(parts) == PageType.PRODUCT


def test_unknown():
    parts = UrlParts.from_url("https://site.com/unknown/page/")
    assert detector.detect(parts) is None
