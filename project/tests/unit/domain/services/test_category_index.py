from project.domain.services.category_index import CategoryIndex
from project.tests.data.categories import all_categories


def test_category_index_single():
    index = CategoryIndex(all_categories)
    assert index.find_categories("/catalogue/elektricheskie-teplye-poly/") == (
        'Напольные покрытия', 'Отопительное оборудование', 'Плитка'
    )


def test_category_index_multiple():
    index = CategoryIndex(all_categories)
    result = index.find_categories("/catalogue/dekor-po-stilyam")
    assert set(result) == {'Декор', 'Текстиль'}


def test_category_index_not_found():
    index = CategoryIndex(all_categories)
    assert index.find_categories("/unknown") == ()
