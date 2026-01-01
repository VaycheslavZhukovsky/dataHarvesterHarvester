from pydantic import BaseModel, field_validator


class SubcategoryUrl(BaseModel):
    url: str

    model_config = {
        "frozen": True,  # делает VO immutable
        "str_strip_whitespace": True,
    }

    @field_validator("url")
    def validate_and_normalize(cls, v: str) -> str:
        if not v.startswith("/"):
            raise ValueError("URL must start with '/'")

        # Убираем слеш в конце, но не корневой "/"
        if len(v) > 1:
            v = v.rstrip("/")

        return v

    def __str__(self) -> str:
        return self.url
