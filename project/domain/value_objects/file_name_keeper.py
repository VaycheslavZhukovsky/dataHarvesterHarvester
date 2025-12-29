from pydantic import BaseModel, field_validator


class FileName(BaseModel):
    name: str

    model_config = {
        "frozen": True,
        "strict": True
    }

    @field_validator("name")
    def check_html_extension(cls, value):
        if not value.endswith(".html"):
            raise ValueError("Файл должен оканчиваться на .html")
        return value
