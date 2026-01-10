class CookiesFileNotFoundError(Exception):
    """The cookies.txt file was not found."""
    pass


class CookiesFileCorruptedError(Exception):
    """The cookies.txt file is corrupted or has an invalid format."""
    pass


class CookiesParsingError(Exception):
    """Error parsing cookies."""
    pass
