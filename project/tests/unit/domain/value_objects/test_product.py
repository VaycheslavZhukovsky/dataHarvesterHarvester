import pytest
from pydantic import ValidationError

from project.domain.value_objects.product import CompareCategory, CharacteristicItem, Characteristics, Source, Brand, \
    MediaMainPhoto, Price, ProductPriceCategory, ProductLink, DisplayedName, ProductId, Category, \
    MeasurementData
from project.tests.data.product import product


# -----------------------------
# ProductPriceCategory
# -----------------------------

def test_product_price_category_creation():
    product_category = ProductPriceCategory(category=product["productPriceCategory"])
    assert product_category.category == "STD"


def test_product_price_category_frozen():
    product_category = ProductPriceCategory(category="Immutable ProductPriceCategory")
    with pytest.raises(ValidationError) as exc_info:
        product_category.category = "New Name"
    assert exc_info.value.errors()[0]['type'] == 'frozen_instance'


# -----------------------------
# Price
# -----------------------------


def test_price_valid():
    price = Price(**product["price"])

    assert price.currency == product["price"]["currency"]
    assert price.main_price == product["price"]["main_price"]


@pytest.mark.parametrize("value", [0, -1, -100])
def test_price_invalid_main_price(value):
    with pytest.raises(ValidationError):
        Price(
            additional_as_main=False,
            currency="RUB",
            main_price=value,
            previous_price=None,
            main_uom="шт",
            main_uom_rus="штука",
            additional_price=None,
            previous_additional_price=None,
            additional_uom=None,
            additional_uom_rus=None,
            discount_percent=None,
            step=1,
        )


@pytest.mark.parametrize("value", ["usd", "rub", "", "ABC"])
def test_price_invalid_currency(value):
    with pytest.raises(ValidationError):
        Price(
            additional_as_main=False,
            currency=value,
            main_price=100,
            previous_price=None,
            main_uom="шт",
            main_uom_rus="штука",
            additional_price=None,
            previous_additional_price=None,
            additional_uom=None,
            additional_uom_rus=None,
            discount_percent=None,
            step=1,
        )


def test_price_is_frozen():
    price = Price(
        additional_as_main=False,
        currency="USD",
        main_price=150,
        previous_price=None,
        main_uom="шт",
        main_uom_rus="штука",
        additional_price=None,
        previous_additional_price=None,
        additional_uom=None,
        additional_uom_rus=None,
        discount_percent=None,
        step=1,
    )

    with pytest.raises(ValidationError):
        price.main_price = 200


# -----------------------------
# ProductLink
# -----------------------------
def test_valid_product_link():
    p = ProductLink(product["productLink"])
    assert p.product_id == 92605778


@pytest.mark.parametrize("link", [
    "",
    "/product/",
    "/product/abc",
    "/product/abc-xyz/",
    "/category/abc-123/",
    "/product/abc-123/extra",
])
def test_invalid_product_link(link):
    with pytest.raises(ValueError):
        ProductLink(link)


# -----------------------------
# DisplayedName
# -----------------------------
def test_displayed_name_creation():
    displayed_name = DisplayedName(name=product["displayedName"])
    assert displayed_name.name == "Обои флизелиновые Wiganford Flowers Language 1.06 м цвет ванильный MK67307"


@pytest.mark.parametrize("value", [
    None,
    "",
    "   ",
])
def test_invalid_displayed_name(value):
    with pytest.raises(ValueError):
        DisplayedName(name=value)


def test_displayed_name_frozen():
    displayed_name = DisplayedName(name="Immutable DisplayedName")
    with pytest.raises(ValidationError) as exc_info:
        displayed_name.name = "New Name"
    assert exc_info.value.errors()[0]['type'] == 'frozen_instance'


# -----------------------------
# mediaMainPhoto
# -----------------------------
invalid_urls_list = [
    # Не https
    {
        "mobile": "http://cdn.lemanapro.ru/path/92605778_01.jpg",
        "tablet": product["mediaMainPhoto"]["tablet"],
        "desktop": product["mediaMainPhoto"]["desktop"]
    },
    # Нет product id
    {
        "mobile": "https://cdn.lemanapro.ru/path/_01.jpg",
        "tablet": product["mediaMainPhoto"]["tablet"],
        "desktop": product["mediaMainPhoto"]["desktop"]
    },
    # Не .jpg
    {
        "mobile": "https://cdn.lemanapro.ru/path/92605778_01",
        "tablet": product["mediaMainPhoto"]["tablet"],
        "desktop": product["mediaMainPhoto"]["desktop"]
    },
]


def test_media_main_photo_valid():
    photo = MediaMainPhoto(**product["mediaMainPhoto"])
    assert photo.mobile == product["mediaMainPhoto"]["mobile"]
    assert photo.tablet == product["mediaMainPhoto"]["tablet"]
    assert photo.desktop == product["mediaMainPhoto"]["desktop"]


@pytest.mark.parametrize("urls", invalid_urls_list)
def test_media_main_photo_invalid(urls):
    with pytest.raises(ValueError):
        MediaMainPhoto(**urls)


# -----------------------------
# Brand
# -----------------------------
def test_brand_creation():
    brand = Brand(name=product["brand"])
    assert brand.name == product["brand"]


def test_brand_frozen():
    brand = Brand(name="Immutable Brand")
    with pytest.raises(ValidationError) as exc_info:
        brand.name = "New Name"
    assert exc_info.value.errors()[0]['type'] == 'frozen_instance'


# -----------------------------
# Source
# -----------------------------
def test_source_creation():
    source = Source(name=product["source"])
    assert source.name == product["source"]


def test_source_frozen():
    source = Source(name="Immutable Source")
    with pytest.raises(ValidationError) as exc_info:
        source.name = "New Name"
    assert exc_info.value.errors()[0]['type'] == 'frozen_instance'


# -----------------------------
# ProductId
# -----------------------------
def test_product_id_creation():
    product_id = ProductId(id=product["productId"])
    assert product_id.id == product["productId"]


def test_product_id_frozen():
    product_id = ProductId(id="Immutable productId")
    with pytest.raises(ValidationError) as exc_info:
        product_id.id = "New Name"
    assert exc_info.value.errors()[0]['type'] == 'frozen_instance'


# -----------------------------
# MeasurementData
# -----------------------------
def test_measurement_data_creation():
    data = MeasurementData(**product["measurementData"])

    assert data.product_measurement_type is None
    assert data.width is None
    assert data.m2_per_box is None


def test_measurement_data_is_frozen():
    data = MeasurementData(**product["measurementData"])

    with pytest.raises(ValidationError):
        data.width = 300


# -----------------------------
# Characteristics
# -----------------------------
def test_characteristics_accepts_list_of_dicts():

    model = Characteristics(characteristics=product["characteristics"])

    assert len(model.characteristics) == 22
    assert isinstance(model.characteristics[0], CharacteristicItem)
    assert model.characteristics[0].key == "06575"
    assert model.characteristics[1].value == "1.06"


def test_characteristics_accepts_list_of_models():
    items = [
        CharacteristicItem(key="001", description="Brand", value="Nike"),
        CharacteristicItem(key="002", description="Width", value="1.06"),
    ]

    model = Characteristics(characteristics=items)

    assert len(model.characteristics) == 2
    assert model.characteristics[0].key == "001"


def test_characteristics_rejects_duplicate_keys():
    data = [
        {"key": "001", "description": "Brand", "value": "Nike"},
        {"key": "001", "description": "Width", "value": "1.06"},
    ]

    with pytest.raises(ValidationError) as exc:
        Characteristics(characteristics=data)

    assert "Keys in characteristics must be unique" in str(exc.value)


# -----------------------------
# CompareCategory
# -----------------------------
def test_compare_category_creation():
    obj = CompareCategory(**product["compareCategory"])
    assert obj.family_id == product["compareCategory"]["familyId"]
    assert obj.name == product["compareCategory"]["name"]


def test_compare_category_is_frozen():
    obj = CompareCategory(familyId="123", name="Обои")
    with pytest.raises(ValidationError):
        obj.family_id = "456"


def test_compare_category_validation_error():
    with pytest.raises(ValidationError):
        CompareCategory(familyId=123, name=None)


# -----------------------------
# Category
# -----------------------------
def test_category_creation():
    category = Category(category=product["category"])
    assert category.category == product["category"]


def test_category_frozen():
    category = Category(category=product["category"])
    with pytest.raises(ValidationError) as exc_info:
        category.category = "New Name"
    assert exc_info.value.errors()[0]['type'] == 'frozen_instance'
