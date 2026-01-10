from pathlib import Path


class FileHtmlReader:
    """Reads HTML from a file."""

    @staticmethod
    def read(path: Path) -> str:
        return path.read_text(encoding="utf-8")
