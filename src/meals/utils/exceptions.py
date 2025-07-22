"""
Exception classes for the meal planner application.
"""

from meals.utils.logger import logger


class MealPlannerException(Exception):
    """Base exception class for the meal planner application."""
    
    def __init__(self, message: str, *args, **kwargs):
        """Initialize the exception."""
        super().__init__(message, *args, **kwargs)
        logger.error(f"{self.__class__.__name__}: {message}")


class DatabaseException(MealPlannerException):
    """Exception raised for database-related errors."""
    
    def __init__(self, message: str, *args, **kwargs):
        """Initialize the exception."""
        super().__init__(f"Database error: {message}", *args, **kwargs)


class ValidationException(MealPlannerException):
    """Exception raised for data validation errors."""
    
    def __init__(self, message: str, *args, **kwargs):
        """Initialize the exception."""
        super().__init__(f"Validation error: {message}", *args, **kwargs)


class UIException(MealPlannerException):
    """Exception raised for UI-related errors."""
    
    def __init__(self, message: str, *args, **kwargs):
        """Initialize the exception."""
        super().__init__(f"UI error: {message}", *args, **kwargs)


class RecoveryException(MealPlannerException):
    """Exception raised for recovery-related errors."""
    
    def __init__(self, message: str, *args, **kwargs):
        """Initialize the exception."""
        super().__init__(f"Recovery error: {message}", *args, **kwargs)