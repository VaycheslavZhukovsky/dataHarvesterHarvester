import json
from pathlib import Path

from project.domain.interfaces.cookies_manager import ICookieProvider


class CookiesManager(ICookieProvider):
    """Создаёт cookies list из cookies.txt"""

    def __init__(self, file_path: Path):
        self.domain = "lemanapro.ru"
        self.path = "/"
        # self.logger = setup_logger(self.__class__.__name__)
        self.cookies: list = []
        self.file_path = file_path

    def build(self) -> list:

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

                if not content.startswith("{"):
                    content = "{" + content + "}"

                data = json.loads(content)

            raw_cookies = data.get("cookies", [])

            for c in raw_cookies:
                if "name" not in c or "value" not in c:
                    # self.logger.warning(f"Некорректный cookie: {c}")
                    continue
                self.cookies.append({
                    "name": c["name"],
                    "value": c["value"],
                    "domain": self.domain,
                    "path": self.path
                })

        except FileNotFoundError as e:
            raise

        except Exception as e:
            # self.logger.error(f"Неизвестная ошибка при обработке cookies: {e}")
            raise

        return self.cookies
