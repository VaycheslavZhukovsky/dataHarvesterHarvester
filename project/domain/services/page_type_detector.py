from project.domain.value_objects.html_obj import UrlParts
from project.domain.value_objects.page_type import PageType


class PageTypeDetector:
    def __init__(self, categories: set[str], subcategories: set[str]):
        self.categories = categories
        self.subcategories = subcategories

    def detect(self, parts: UrlParts) -> PageType | None:
        seg = parts.segments

        if not seg:
            return None

        # product/sku123
        if seg[0] == "product":
            return PageType.PRODUCT

        # catalogue/<page>
        if len(seg) >= 2 and seg[0] == "catalogue":
            page = seg[1]

            if page in self.categories:
                return PageType.CATEGORY

            if page in self.subcategories:
                return PageType.SUBCATEGORY

        return None
