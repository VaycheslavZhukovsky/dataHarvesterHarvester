import json
from pathlib import Path

from project.domain.interfaces.ICookieProvider import ICookieProvider
from project.infrastructure.exceptions.cookies_exceptions import CookiesFileNotFoundError, CookiesParsingError, \
    CookiesFileCorruptedError
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


class CookiesManager(ICookieProvider):
    """Creates a list of cookies from cookies.txt suitable for Playwright."""

    def __init__(self, file_path: Path):
        self.domain = "krasnodar.lemanapro.ru"
        self.path = "/"
        self.cookies: list = []
        self.file_path = file_path

    def build(self) -> list:
        logger.debug(f"Loading cookies from: {self.file_path}")

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

        except FileNotFoundError as e:
            logger.error(f"Cookies file not found: {self.file_path}")
            raise CookiesFileNotFoundError(
                f"Cookies file not found: {self.file_path}"
            ) from e

        # Попытка привести к JSON
        try:
            if not content.startswith("{"):
                logger.warning("Cookies file missing outer braces. Fixing automatically.")
                content = "{" + content + "}"

            data = json.loads(content)

        except json.JSONDecodeError as e:
            logger.error(f"Cookies file corrupted or invalid JSON: {e}")
            raise CookiesFileCorruptedError(
                f"Invalid JSON in cookies file: {self.file_path}"
            ) from e

        try:
            raw_cookies = data.get("cookies", [])

            for c in raw_cookies:
                if "name" not in c or "value" not in c:
                    logger.warning(f"Skipping malformed cookie entry: {c}")
                    continue

                self.cookies.append({
                    "name": c["name"],
                    "value": c["value"],
                    "domain": self.domain,
                    "path": self.path,
                })

        except Exception as e:
            logger.exception("Unexpected error while parsing cookies")
            raise CookiesParsingError(
                f"Unexpected error while parsing cookies: {e}"
            ) from e

        logger.info(f"Loaded {len(self.cookies)} cookies from {self.file_path}")
        return self.cookies
