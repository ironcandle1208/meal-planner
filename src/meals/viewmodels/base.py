"""
Base ViewModel for the meal planner application.
"""

from abc import ABC
from typing import Any, Callable, Dict, List, Optional

import toga
from toga.style import Pack

from meals.utils.exceptions import MealPlannerException, ValidationException


class BaseViewModel(ABC):
    """Base ViewModel for all ViewModels."""
    
    def __init__(self):
        """Initialize the ViewModel."""
        self._error_handlers: Dict[str, Callable[[Exception], None]] = {}
        self._success_handlers: Dict[str, Callable[[Any], None]] = {}
    
    def register_error_handler(self, action: str, handler: Callable[[Exception], None]) -> None:
        """Register an error handler for an action."""
        self._error_handlers[action] = handler
    
    def register_success_handler(self, action: str, handler: Callable[[Any], None]) -> None:
        """Register a success handler for an action."""
        self._success_handlers[action] = handler
    
    def _handle_error(self, action: str, error: Exception) -> None:
        """Handle an error."""
        if action in self._error_handlers:
            self._error_handlers[action](error)
        else:
            # Default error handling
            print(f"Error in {action}: {str(error)}")
    
    def _handle_success(self, action: str, result: Any = None) -> None:
        """Handle a success."""
        if action in self._success_handlers:
            self._success_handlers[action](result)
    
    def show_error_dialog(self, window: toga.Window, title: str, message: str) -> None:
        """Show an error dialog."""
        window.info_dialog(title, message)
    
    def show_success_dialog(self, window: toga.Window, title: str, message: str) -> None:
        """Show a success dialog."""
        window.info_dialog(title, message)
    
    def show_confirmation_dialog(self, window: toga.Window, title: str, message: str) -> bool:
        """Show a confirmation dialog."""
        return window.question_dialog(title, message)
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> None:
        """Validate that required fields are present and not empty."""
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationException(f"Missing required fields: {', '.join(missing_fields)}")