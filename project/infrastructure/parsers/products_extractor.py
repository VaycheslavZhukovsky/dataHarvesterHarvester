import json5
from typing import List

from project.infrastructure.exceptions.parsing_errors import (
    JsonBlockNotFoundError,
    JsonExtractionError,
    ProductsDataNotFoundError,
    ProductsDataMalformedError,
)
from project.domain.interfaces.IProductsExtractor import IProductsExtractor
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class ProductsExtractor(IProductsExtractor):

    def __init__(self, start_marker: str = 'window.INITIAL_STATE["plp"]'):
        self.start_marker = start_marker
        logger.debug(f"ProductsExtractor initialized with start_marker={start_marker}")

    def extract_json_from_garbage(self, text: str) -> str:
        logger.debug("Starting JSON extraction from garbage")

        start = text.find("{")
        if start == -1:
            logger.error("Opening '{' not found in text")
            raise JsonExtractionError("No '{' found in text")

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
                        logger.debug("Successfully extracted JSON block")
                        return text[start:i+1]

            escape = (ch == "\\" and not escape)

        logger.error("JSON braces not balanced")
        raise JsonExtractionError("JSON braces not balanced")

    def extract_products_data(self, json_text: str) -> str:
        logger.debug("Extracting productsData array")

        key = '"productsData"'
        pos = json_text.find(key)
        if pos == -1:
            logger.error("productsData key not found")
            raise ProductsDataNotFoundError("productsData not found")

        start = json_text.find("[", pos)
        if start == -1:
            logger.error("productsData '[' not found")
            raise ProductsDataMalformedError("productsData array '[' not found")

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
                        logger.debug("productsData array successfully extracted")
                        return json_text[start:i+1]

            escape = (ch == "\\" and not escape)

        logger.error("productsData array not closed")
        raise ProductsDataMalformedError("productsData array not closed")

    def extract_json_from_html_str(self, html: str) -> str | None:
        logger.debug("Searching for start_marker in HTML")

        pos = html.find(self.start_marker)
        if pos == -1:
            logger.warning("start_marker not found in HTML")
            return None

        logger.debug("start_marker found, extracting JSON block")
        tail = html[pos:]
        return self.extract_json_from_garbage(tail)

    def create_products_list_from_str(self, html: str) -> List[dict]:
        logger.debug("Creating products list from HTML string")

        json_str = self.extract_json_from_html_str(html)
        if json_str is None:
            logger.error("INITIAL_STATE['plp'] block not found")
            raise JsonBlockNotFoundError("INITIAL_STATE['plp'] not found")

        products_json = self.extract_products_data(json_str)

        logger.debug("Parsing products JSON into Python objects")
        return json5.loads(products_json)
