from typing import Dict, List, Set, Tuple

from project.domain.value_objects.subcategory_url import SubcategoryUrl


class CategoryIndex:
    """
    Domain Service, который хранит связи:
        категория → подкатегории
        подкатегория (VO) → категории
    """

    def __init__(self, data: Dict[str, List[Dict[str, str]]]):
        self._sub_to_categories: Dict[SubcategoryUrl, Set[str]] = {}

        for category, subcategories in data.items():
            for sub in subcategories:
                url = SubcategoryUrl(url=sub["url"])
                self._sub_to_categories.setdefault(url, set()).add(category)

    def find_categories(self, subcategory_url: str) -> Tuple[str, ...]:
        url = SubcategoryUrl(url=subcategory_url)
        categories = self._sub_to_categories.get(url, [])
        return tuple(sorted(categories))
