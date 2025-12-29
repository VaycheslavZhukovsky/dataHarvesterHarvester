from dataclasses import dataclass

from project.domain.value_objects.product import ProductId, Price, ProductPriceCategory, ProductLink, DisplayedName, \
    Eligibility, MediaMainPhoto, Brand, Source, MeasurementData, Characteristics, Category, CompareCategory


@dataclass
class Product:
    product_price_category: ProductPriceCategory
    price: Price
    product_link: ProductLink
    displayed_name: DisplayedName
    eligibility: Eligibility
    media_main_photo: MediaMainPhoto
    brand: Brand
    source: Source
    product_id: ProductId
    measurement_data: MeasurementData
    characteristics: Characteristics
    compare_category: CompareCategory
    category: Category
