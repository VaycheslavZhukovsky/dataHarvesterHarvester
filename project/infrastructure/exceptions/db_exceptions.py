
class CategoryNotFoundError(Exception):
    """Категория с таким slug не найдена в БД."""


class DatabaseOperationError(Exception):
    """Ошибка при выполнении операции с БД."""


class DatabaseConnectionError(Exception):
    """Ошибка подключения к базе данных."""
