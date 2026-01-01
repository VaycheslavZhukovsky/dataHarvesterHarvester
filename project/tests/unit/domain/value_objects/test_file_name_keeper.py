import pytest
from pydantic import ValidationError

from project.domain.value_objects.file_name_keeper import FileName


def test_valid_html_extension():
    obj = FileName(name="index.html")
    assert obj.name == "index.html"


def test_invalid_extension():
    with pytest.raises(ValidationError):
        FileName(name="index.txt")


def test_no_extension():
    with pytest.raises(ValidationError):
        FileName(name="file")
