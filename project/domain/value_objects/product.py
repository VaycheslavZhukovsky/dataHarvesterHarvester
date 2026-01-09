import re
from dataclasses import dataclass
from typing import Optional, List, Any

from pydantic import BaseModel, Field, model_validator, field_validator


class ProductPriceCategory(BaseModel):
    category: Optional[str]

    model_config = {
        "frozen": True
    }


class Price(BaseModel):
    additional_as_main: bool
    currency: str
    main_price: float
    previous_price: Optional[float]
    main_uom: str
    main_uom_rus: str
    additional_price: Optional[float]
    previous_additional_price: Optional[float]
    additional_uom: Optional[str]
    additional_uom_rus: Optional[str]
    discount_percent: Optional[float]
    step: int

    model_config = {
        "frozen": True
    }

    @field_validator("main_price")
    def validate_main_price(cls, value: int):
        if value <= 0:
            raise ValueError("main_price must be > 0")
        return value

    @field_validator("currency")
    def validate_currency(cls, value: str):
        allowed = {"RUB", "USD", "EUR"}
        if value not in allowed:
            raise ValueError(f"currency must be one of {allowed}")
        return value


PRODUCT_LINK_PATTERN = re.compile(r"^/product/.+?-(\d+)/?$")


@dataclass(frozen=True)
class ProductLink:
    link: str

    def __post_init__(self):
        if not self.link:
            raise ValueError("link cannot be empty")

        match = PRODUCT_LINK_PATTERN.match(self.link)
        if not match:
            raise ValueError(f"Invalid product link format: {self.link}")

    @property
    def product_id(self) -> int:

        """Извлекаем ID, но это уже удобный бонус."""
        match = PRODUCT_LINK_PATTERN.match(self.link)
        return int(match.group(1))


class DisplayedName(BaseModel):
    name: str

    model_config = {
        "frozen": True,
        "strict": True,
    }

    @field_validator("name", mode="after")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("DisplayedName cannot be empty")
        return v


class MediaMainPhoto(BaseModel):
    mobile: str
    tablet: str
    desktop: str

    model_config = {
        "frozen": True  # аналог frozen dataclass
    }


class Brand(BaseModel):
    name: Optional[str]

    model_config = {
        "frozen": True,
    }


class Source(BaseModel):
    name: str

    model_config = {
        "frozen": True
    }


class ProductId(BaseModel):
    id: str

    model_config = {
        "frozen": True
    }


class MeasurementData(BaseModel):
    product_measurement_type: Any = Field(..., alias="productMeasurementType")
    width: Any
    m2_per_box: Any = Field(..., alias="m2PerBox")

    model_config = {
        "frozen": True,
        "populate_by_name": True
    }


class CharacteristicItem(BaseModel):
    key: str
    description: str
    value: str

    model_config = {
        "frozen": True
    }


class Characteristics(BaseModel):
    characteristics: List[CharacteristicItem]

    @model_validator(mode="before")
    def normalize_and_validate(cls, values):
        raw_items = values.get("characteristics", [])

        items = [
            item if isinstance(item, CharacteristicItem) else CharacteristicItem(**item)
            for item in raw_items
        ]

        keys = [item.key for item in items]
        if len(keys) != len(set(keys)):
            raise ValueError("Keys in characteristics must be unique")

        return {"characteristics": items}


class CompareCategory(BaseModel):
    family_id: Optional[str] = Field(..., alias="familyId", description="ID семьи товара")
    name: Optional[str] = Field(..., description="Название категории")

    model_config = {
        "frozen": True,
        "populate_by_name": True
    }


class Category(BaseModel):
    category: str | None

    model_config = {
        "frozen": True
    }
