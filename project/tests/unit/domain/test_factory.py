from project.domain.handlers.CategoryHandler import CategoryHandler
from project.domain.handlers.PageHandlerFactory import PageHandlerFactory
from project.domain.handlers.ProductHandler import ProductHandler
from project.domain.handlers.SubcategoryHandler import SubcategoryHandler
from project.domain.value_objects.PageType import PageType

factory = PageHandlerFactory()


def test_factory_category():
    assert isinstance(factory.create(PageType.CATEGORY), CategoryHandler)


def test_factory_subcategory():
    assert isinstance(factory.create(PageType.SUBCATEGORY), SubcategoryHandler)


def test_factory_product():
    assert isinstance(factory.create(PageType.PRODUCT), ProductHandler)
