import json
import pytest
from pathlib import Path

from project.infrastructure.playwright.cookies_manager import CookiesManager


@pytest.fixture
def tmp_file(tmp_path: Path):
    """Утилита для создания временного файла."""
    def _create(content: str) -> Path:
        p = tmp_path / "cookies.txt"
        p.write_text(content, encoding="utf-8")
        return p
    return _create


def test_build_valid_cookies(tmp_file):
    """Корректный JSON → корректный список cookies."""
    file = tmp_file(json.dumps({
        "cookies": [
            {"name": "sid", "value": "123"},
            {"name": "token", "value": "abc"},
        ]
    }))

    cm = CookiesManager(file)
    result = cm.build()

    assert result == [
        {"name": "sid", "value": "123", "domain": "lemanapro.ru", "path": "/"},
        {"name": "token", "value": "abc", "domain": "lemanapro.ru", "path": "/"},
    ]


def test_build_without_braces(tmp_file):
    """Если файл не начинается с '{', менеджер добавляет фигурные скобки."""
    file = tmp_file('"cookies": [{"name": "a", "value": "b"}]')

    cm = CookiesManager(file)
    result = cm.build()

    assert result == [
        {"name": "a", "value": "b", "domain": "lemanapro.ru", "path": "/"},
    ]


def test_build_skips_invalid_cookie_entries(tmp_file):
    """Cookie без name или value пропускаются."""
    file = tmp_file(json.dumps({
        "cookies": [
            {"name": "ok", "value": "1"},
            {"name": "missing_value"},
            {"value": "missing_name"},
            {"foo": "bar"},
        ]
    }))

    cm = CookiesManager(file)
    result = cm.build()

    assert result == [
        {"name": "ok", "value": "1", "domain": "lemanapro.ru", "path": "/"},
    ]


def test_build_empty_list(tmp_file):
    """Если cookies пустые — возвращается пустой список."""
    file = tmp_file(json.dumps({"cookies": []}))

    cm = CookiesManager(file)
    result = cm.build()

    assert result == []


def test_build_no_cookies_key(tmp_file):
    """Если ключа cookies нет — возвращается пустой список."""
    file = tmp_file(json.dumps({"foo": "bar"}))

    cm = CookiesManager(file)
    result = cm.build()

    assert result == []


def test_build_file_not_found():
    """Отсутствие файла → FileNotFoundError пробрасывается."""
    cm = CookiesManager(Path("/non/existent/file.txt"))

    with pytest.raises(FileNotFoundError):
        cm.build()


def test_build_invalid_json(tmp_file):
    """Битый JSON → исключение пробрасывается."""
    file = tmp_file("{invalid json")

    cm = CookiesManager(file)

    with pytest.raises(Exception):
        cm.build()
