
class CategoryNotFoundError(Exception):
    """A category with this slug was not found in the database."""


class DatabaseOperationError(Exception):
    """An error occurred while performing the database operation."""


class DatabaseConnectionError(Exception):
    """Ошибка подключения к базе данных."""
