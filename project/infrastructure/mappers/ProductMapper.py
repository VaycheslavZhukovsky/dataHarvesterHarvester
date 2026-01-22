from pydantic import ValidationError

from project.domain.entities.Product import Product
from project.domain.exceptions.ProductError import ValueObjectProductValidationError
from project.domain.value_objects.product import ProductPriceCategory, Price, ProductLink, DisplayedName, \
    MediaMainPhoto, Brand, Source, ProductId, MeasurementData, Characteristics, CompareCategory, Category
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ProductMapper:
    @staticmethod
    def asemble_entity(raw: dict) -> Product:
        try:
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

        except ValidationError as exc:
            logger.exception(f"Product validation error: {raw['productId']}")
            raise ValueObjectProductValidationError(
                f"Mapping error Product: {exc}"
            ) from exc

    @staticmethod
    def asemble_entities(rows: list[dict]) -> list[Product]:
        return [ProductMapper.asemble_entity(row) for row in rows]
