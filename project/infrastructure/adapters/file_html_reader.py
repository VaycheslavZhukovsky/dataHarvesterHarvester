from pathlib import Path


class FileHtmlReader:
    """Читает HTML из файла."""

    @staticmethod
    def read(path: Path) -> str:
        return path.read_text(encoding="utf-8")
