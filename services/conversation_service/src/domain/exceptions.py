"""Domain exceptions.

This module defines common exceptions used throughout the domain layer
following Domain-Driven Design principles.
"""

class DomainException(Exception):
    """Base exception for all domain-related errors.

    This is the parent class for all domain-specific exceptions in the system.
    It can be used to catch any domain error regardless of its specific type.
    """

    pass


class ValidationError(DomainException):
    """Exception raised when domain validation fails.

    This exception is raised when an entity or value object fails validation,
    such as when required fields are missing or business rules are violated.
    """

    pass


class EntityNotFoundError(DomainException):
    """Exception raised when an entity cannot be found.

    This exception is raised when an attempt is made to retrieve or operate
    on an entity that does not exist in the system.
    """

    pass


class PermissionError(DomainException):
    """Exception raised when an operation is not permitted.

    This exception is raised when a user attempts an operation they do not
    have permission to perform, such as accessing another user's resources.
    """

    pass


class BusinessRuleViolationError(DomainException):
    """Exception raised when a business rule is violated.

    This exception is raised when an operation would violate a business rule
    or invariant of the domain, such as exceeding limits or breaking constraints.
    """

    pass


class RepositoryError(DomainException):
    """Exception raised when a repository operation fails.

    This exception is raised when there's an error in the persistence layer,
    such as database connection failures or constraint violations.
    """

    pass


class EventPublishingError(DomainException):
    """Exception raised when publishing domain events fails.

    This exception is raised when there's an error in the event publishing
    mechanism, such as message broker connectivity issues.
    """

    pass
