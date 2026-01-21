class DatabaseError(Exception):
    """A category with this slug was not found in the database."""


class CategoryNotFoundError(DatabaseError):
    """A category with this slug was not found in the database."""


class DatabaseOperationError(DatabaseError):
    """An error occurred while performing the database operation."""


class DatabaseConnectionError(DatabaseError):
    """Ошибка подключения к базе данных."""
