"""
Views package for the meal planner application.
"""

from meals.views.main_window import MainView
from meals.views.meal_plan import MealPlanView
from meals.views.recipe import RecipeView
from meals.views.shopping_list import ShoppingListView

__all__ = [
    "MainView",
    "MealPlanView",
    "RecipeView",
    "ShoppingListView",
]