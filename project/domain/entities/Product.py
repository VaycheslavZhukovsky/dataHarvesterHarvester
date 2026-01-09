from dataclasses import dataclass

from project.domain.value_objects.product import ProductId, Price, ProductPriceCategory, ProductLink, DisplayedName, \
    MediaMainPhoto, Brand, Source, MeasurementData, Characteristics, Category, CompareCategory


@dataclass
class Product:
    product_id: ProductId
    price: Price
    product_price_category: ProductPriceCategory
    category: Category
    brand: Brand
    displayed_name: DisplayedName
    source: Source
    measurement_data: MeasurementData
    characteristics: Characteristics
    compare_category: CompareCategory
    product_link: ProductLink
    media_main_photo: MediaMainPhoto
