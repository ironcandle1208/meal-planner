"""
Main window view for the meal planner application.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from meals.utils.exceptions import MealPlannerException


class MainView:
    """Main window view for the meal planner application."""
    
    def __init__(self, app):
        """Initialize the main window view."""
        self.app = app
        self.main_box = None
        self.tabs = None
        
        # Views
        self.meal_plan_view = None
        self.recipe_view = None
        self.shopping_list_view = None
        
        # Create the main window
        self._create_main_window()
    
    def _create_main_window(self):
        """Create the main window."""
        # Main container
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        
        # Import views here to avoid circular imports
        from meals.views.meal_plan import MealPlanView
        from meals.views.recipe import RecipeView
        from meals.views.shopping_list import ShoppingListView
        
        # Create views
        self.meal_plan_view = MealPlanView(self.app)
        self.recipe_view = RecipeView(self.app)
        self.shopping_list_view = ShoppingListView(self.app)
        
        # Create tab container with content
        self.tabs = toga.OptionContainer(
            style=Pack(flex=1),
            content=[
                ("献立", self.meal_plan_view.content),
                ("レシピ", self.recipe_view.content),
                ("買い物リスト", self.shopping_list_view.content),
            ]
        )
        
        # Add tabs to main box
        self.main_box.add(self.tabs)
        
        # Set main window content
        self.app.main_window.content = self.main_box
    
    def show_error(self, title, message):
        """Show an error dialog."""
        self.app.main_window.info_dialog(title, message)
    
    def show_success(self, title, message):
        """Show a success dialog."""
        self.app.main_window.info_dialog(title, message)
    
    def show_confirmation(self, title, message):
        """Show a confirmation dialog."""
        return self.app.main_window.question_dialog(title, message)