from project.domain.handlers.CategoryHandler import CategoryHandler
from project.domain.handlers.ProductHandler import ProductHandler
from project.domain.handlers.SubcategoryHandler import SubcategoryHandler
from project.domain.value_objects.PageType import PageType


class PageHandlerFactory:
    def create(self, page_type: PageType):
        match page_type:
            case PageType.CATEGORY:
                return CategoryHandler()
            case PageType.SUBCATEGORY:
                return SubcategoryHandler()
            case PageType.PRODUCT:
                return ProductHandler()
        raise ValueError(f"Unknown page type: {page_type}")
