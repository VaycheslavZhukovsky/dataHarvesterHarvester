from project.domain.entities.product import Product
from project.domain.value_objects.product import ProductPriceCategory, Price, ProductLink, DisplayedName, Eligibility, \
    MediaMainPhoto, Brand, Source, ProductId, MeasurementData, Characteristics, CompareCategory, Category


class ProductMapper:
    def to_entity(self, raw: dict) -> Product:
        return Product(
            product_price_category=ProductPriceCategory(category=raw["productPriceCategory"]),
            price=Price(**raw["price"]),
            product_link=ProductLink(raw["productLink"]),
            displayed_name=DisplayedName(name=raw["displayedName"]),
            eligibility=Eligibility(**raw["eligibility"]),
            media_main_photo=MediaMainPhoto(**raw["mediaMainPhoto"]),
            brand=Brand(name=raw["brand"]),
            source=Source(name=raw["source"]),
            product_id=ProductId(id=raw["productId"]),
            measurement_data=MeasurementData(**raw["measurementData"]),
            characteristics=Characteristics(characteristics=raw["characteristics"]),
            compare_category=CompareCategory(**raw["compareCategory"]),
            category=Category(category=raw["category"])
        )
