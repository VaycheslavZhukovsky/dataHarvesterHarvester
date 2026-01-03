from project.domain.handlers.category_handler import CategoryHandler
from project.domain.handlers.factory import PageHandlerFactory
from project.domain.handlers.product_handler import ProductHandler
from project.domain.handlers.subcategory_handler import SubcategoryHandler
from project.domain.value_objects.page_type import PageType

factory = PageHandlerFactory()


def test_factory_category():
    assert isinstance(factory.create(PageType.CATEGORY), CategoryHandler)


def test_factory_subcategory():
    assert isinstance(factory.create(PageType.SUBCATEGORY), SubcategoryHandler)


def test_factory_product():
    assert isinstance(factory.create(PageType.PRODUCT), ProductHandler)
