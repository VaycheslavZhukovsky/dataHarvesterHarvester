import pytest

from project.domain.value_objects.SubcategoryUrl import SubcategoryUrl


def test_value_object_normalization():
    url1 = SubcategoryUrl(url="/catalogue/elektricheskie-teplye-poly")
    url2 = SubcategoryUrl(url="/catalogue/elektricheskie-teplye-poly/")
    assert url1 == url2
    assert str(url1) == "/catalogue/elektricheskie-teplye-poly"


def test_value_object_invalid():
    with pytest.raises(ValueError):
        SubcategoryUrl(url="catalogue/elektricheskie-teplye-poly")  # нет ведущего "/"

