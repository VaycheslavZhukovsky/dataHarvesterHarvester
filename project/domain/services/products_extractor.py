import json5
from typing import List

from project.domain.interfaces.product_extractor import IProductsExtractor


class ProductsExtractor(IProductsExtractor):
    """
    Чистый парсер: принимает HTML строку, возвращает список dict.
    Не знает про Path, файлы, Playwright, сеть.
    """

    def __init__(self, start_marker: str = 'window.INITIAL_STATE["plp"]'):
        self.start_marker = start_marker

    def extract_json_from_garbage(self, text: str) -> str:
        start = text.find("{")
        if start == -1:
            raise ValueError("No '{' found in text")

        brace_count = 0
        in_string = False
        escape = False

        for i in range(start, len(text)):
            ch = text[i]

            if ch == '"' and not escape:
                in_string = not in_string

            if not in_string:
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        return text[start:i+1]

            escape = (ch == "\\" and not escape)

        raise ValueError("JSON braces not balanced")

    def extract_products_data(self, json_text: str) -> str:
        key = '"productsData"'
        pos = json_text.find(key)
        if pos == -1:
            raise ValueError("productsData not found")

        start = json_text.find("[", pos)
        if start == -1:
            raise ValueError("productsData array '[' not found")

        bracket_count = 0
        in_string = False
        escape = False

        for i in range(start, len(json_text)):
            ch = json_text[i]

            if ch == '"' and not escape:
                in_string = not in_string

            if not in_string:
                if ch == "[":
                    bracket_count += 1
                elif ch == "]":
                    bracket_count -= 1
                    if bracket_count == 0:
                        return json_text[start:i+1]

            escape = (ch == "\\" and not escape)

        raise ValueError("productsData array not closed")

    def extract_json_from_html_str(self, html: str) -> str | None:
        pos = html.find(self.start_marker)
        if pos == -1:
            return None

        tail = html[pos:]
        return self.extract_json_from_garbage(tail)

    def create_products_list_from_str(self, html: str) -> List[dict]:
        json_str = self.extract_json_from_html_str(html)
        if json_str is None:
            raise ValueError("INITIAL_STATE['plp'] not found")

        products_json = self.extract_products_data(json_str)
        return json5.loads(products_json)
