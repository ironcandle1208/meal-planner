"""
Schemas package for the meal planner application.
"""

from meals.schemas.base import BaseSchema
from meals.schemas.meal_plan import MealPlanCreate, MealPlanRead, MealPlanUpdate
from meals.schemas.recipe import IngredientCreate, IngredientRead, RecipeCreate, RecipeRead, RecipeUpdate
from meals.schemas.shopping_list import (
    ShoppingListCreate,
    ShoppingListItemCreate,
    ShoppingListItemRead,
    ShoppingListItemUpdate,
    ShoppingListRead,
    ShoppingListUpdate,
)

__all__ = [
    "BaseSchema",
    "MealPlanCreate",
    "MealPlanRead",
    "MealPlanUpdate",
    "RecipeCreate",
    "RecipeRead",
    "RecipeUpdate",
    "IngredientCreate",
    "IngredientRead",
    "ShoppingListCreate",
    "ShoppingListRead",
    "ShoppingListUpdate",
    "ShoppingListItemCreate",
    "ShoppingListItemRead",
    "ShoppingListItemUpdate",
]