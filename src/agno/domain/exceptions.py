"""Custom exceptions for the domain layer."""


class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class SearchException(DomainException):
    """Exception raised when search fails."""
    pass


class ScrapingException(DomainException):
    """Exception raised when content scraping fails."""
    pass


class BlogGenerationException(DomainException):
    """Exception raised when blog generation fails."""
    pass


class CacheException(DomainException):
    """Exception raised when cache operations fail."""
    pass
