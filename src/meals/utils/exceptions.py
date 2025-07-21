"""
Exception classes for the meal planner application.
"""


class MealPlannerException(Exception):
    """Base exception class for the meal planner application."""
    pass


class DatabaseException(MealPlannerException):
    """Exception raised for database-related errors."""
    pass


class ValidationException(MealPlannerException):
    """Exception raised for data validation errors."""
    pass


class UIException(MealPlannerException):
    """Exception raised for UI-related errors."""
    pass