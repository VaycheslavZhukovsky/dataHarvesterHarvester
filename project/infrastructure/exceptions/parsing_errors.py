class ParsingError(Exception):
    """Base class for all parsing-related errors."""
    pass


class JsonBlockNotFoundError(ParsingError):
    """Raised when INITIAL_STATE['plp'] block is not found."""
    pass


class JsonExtractionError(ParsingError):
    """Raised when JSON braces are unbalanced or malformed."""
    pass


class ProductsDataNotFoundError(ParsingError):
    """Raised when 'productsData' array is missing."""
    pass


class ProductsDataMalformedError(ParsingError):
    """Raised when 'productsData' array is not properly closed."""
    pass
