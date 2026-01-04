import pytest

from project.domain.entities.product import Product
from project.domain.value_objects.product import ProductPriceCategory, Price, ProductLink, DisplayedName, \
    MediaMainPhoto, Brand, Source, ProductId, MeasurementData, Characteristics, CompareCategory, Category
from project.tests.data.product import product


@pytest.fixture
def product_data():
    return {
        "product_price_category": ProductPriceCategory(category=product["productPriceCategory"]),
        "price": Price(**product["price"]),
        "product_link": ProductLink(product["productLink"]),
        "displayed_name": DisplayedName(name=product["displayedName"]),
        "media_main_photo": MediaMainPhoto(**product["mediaMainPhoto"]),
        "brand": Brand(name=product["brand"]),
        "source": Source(name=product["source"]),
        "product_id": ProductId(id=product["productId"]),
        "measurement_data": MeasurementData(**product["measurementData"]),
        "characteristics": Characteristics(characteristics=product["characteristics"]),
        "compare_category": CompareCategory(**product["compareCategory"]),
        "category": Category(category=product["category"]),
    }


def test_product_initialization(product_data):
    """Проверка корректного создания объекта."""
    product = Product(**product_data)
    assert isinstance(product, Product)
    for field, value in product_data.items():
        assert getattr(product, field) == value


def test_product_equality(product_data):
    """dataclass должен корректно сравнивать экземпляры."""
    p1 = Product(**product_data)
    p2 = Product(**product_data)
    assert p1 == p2
