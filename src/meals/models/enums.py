"""
Enum definitions for the meal planner application.
"""

from enum import Enum, auto


class MealType(str, Enum):
    """Meal type enum."""
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"


class RecipeCategory(str, Enum):
    """Recipe category enum."""
    MAIN_DISH = "MAIN_DISH"
    SIDE_DISH = "SIDE_DISH"
    SOUP = "SOUP"
    SALAD = "SALAD"
    DESSERT = "DESSERT"
    DRINK = "DRINK"
    OTHER = "OTHER"


class IngredientCategory(str, Enum):
    """Ingredient category enum."""
    VEGETABLE = "VEGETABLE"
    MEAT = "MEAT"
    FISH = "FISH"
    DAIRY = "DAIRY"
    GRAIN = "GRAIN"
    FRUIT = "FRUIT"
    SPICE = "SPICE"
    CONDIMENT = "CONDIMENT"
    OTHER = "OTHER"