from project.domain.handlers.category_handler import CategoryHandler
from project.domain.handlers.product_handler import ProductHandler
from project.domain.handlers.subcategory_handler import SubcategoryHandler
from project.domain.value_objects.page_type import PageType


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
