from project.domain.entities.product import Product
from project.domain.value_objects.product import ProductPriceCategory, Price, ProductLink, DisplayedName, \
    MediaMainPhoto, Brand, Source, ProductId, MeasurementData, Characteristics, CompareCategory, Category


class ProductMapper:
    @staticmethod
    def to_entity(raw: dict) -> Product:
        return Product(
            product_price_category=ProductPriceCategory(category=raw["productPriceCategory"]),
            price=Price(**raw["price"]),
            product_link=ProductLink(raw["productLink"]),
            displayed_name=DisplayedName(name=raw["displayedName"]),
            media_main_photo=MediaMainPhoto(**raw["mediaMainPhoto"]),
            brand=Brand(name=raw["brand"]),
            source=Source(name=raw["source"]),
            product_id=ProductId(id=raw["productId"]),
            measurement_data=MeasurementData(**raw["measurementData"]),
            characteristics=Characteristics(characteristics=raw["characteristics"]),
            compare_category=CompareCategory(**raw["compareCategory"]),
            category=Category(category=raw["category"])
        )

    @staticmethod
    def to_entities(rows: list[dict]) -> list[Product]:
        return [ProductMapper.to_entity(row) for row in rows]
