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


class JsonParsingError(ParsingError):
    """Raised when JSON block is found but cannot be parsed."""
    pass


class OfferCountMissingError(ParsingError):
    """Raised when 'offerCount' is missing in JSON-LD."""
    pass


class OfferCountInvalidError(ParsingError):
    """Raised when 'offerCount' exists but has invalid type/value."""
    pass
