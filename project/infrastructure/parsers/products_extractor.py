from pathlib import Path
from typing import List

import json5


class ProductsExtractor:
    def __init__(self, start_marker='window.INITIAL_STATE["plp"]'):
        self.start_marker = start_marker

    # -----------------------------
    # 1. Извлекаем JSON из мусора
    # -----------------------------
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

    # -----------------------------------------
    # 2. Извлекаем массив productsData из JSON
    # -----------------------------------------
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

    # -----------------------------------------------------
    # 3. Читаем HTML, находим блок, извлекаем JSON-объект
    # -----------------------------------------------------
    def extract_json_from_html(self, html_path: Path) -> str | None:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        pos = html.find(self.start_marker)
        if pos == -1:
            return None

        tail = html[pos:]
        return self.extract_json_from_garbage(tail)

    # -----------------------------------------------------
    # 4. Финальная функция: получить productsData как текст
    # -----------------------------------------------------
    def create_products_list(self, html_path: Path) -> List[dict]:
        json_str = self.extract_json_from_html(html_path)
        if json_str is None:
            raise ValueError("INITIAL_STATE['plp'] not found")

        return json5.loads(self.extract_products_data(json_str))
