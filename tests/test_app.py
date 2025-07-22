"""
Tests for the app module.
"""

import unittest
from unittest.mock import MagicMock, patch

import toga
from toga.sources import Source

from meals.app import MealPlannerApp


class TestApp(unittest.TestCase):
    """Tests for the app module."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a mock app
        self.app = MealPlannerApp("献立管理", "com.example.meals")
        self.app.main_window = MagicMock()
    
    def test_app_initialization(self):
        """Test app initialization."""
        # Call startup
        with patch("meals.app.MainView") as mock_main_view:
            with patch("meals.utils.database.init_db") as mock_init_db:
                self.app.startup()
                
                # Check if init_db was called
                mock_init_db.assert_called_once()
                
                # Check if MainView was created
                mock_main_view.assert_called_once_with(self.app)
    
    def test_app_initialization_error(self):
        """Test app initialization with an error."""
        # Call startup
        with patch("meals.app.MainView") as mock_main_view:
            with patch("meals.utils.database.init_db") as mock_init_db:
                # Make init_db raise an exception
                mock_init_db.side_effect = Exception("Test error")
                
                self.app.startup()
                
                # Check if init_db was called
                mock_init_db.assert_called_once()
                
                # Check if info_dialog was called
                self.app.main_window.info_dialog.assert_called_once()
                
                # Check if MainView was not created
                mock_main_view.assert_not_called()


if __name__ == "__main__":
    unittest.main()