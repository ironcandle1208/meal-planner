"""
Tests for the models module.
"""

import datetime
import unittest
from datetime import date

from meals.models import Ingredient, MealPlan, Recipe, ShoppingList, ShoppingListItem
from meals.models.enums import IngredientCategory, MealType, RecipeCategory


class TestModels(unittest.TestCase):
    """Tests for the models module."""
    
    def test_meal_plan_creation(self):
        """Test creating a MealPlan."""
        meal_plan = MealPlan(
            name="朝食メニュー",
            date=date.today(),
            meal_type=MealType.BREAKFAST.value,
        )
        
        self.assertEqual(meal_plan.name, "朝食メニュー")
        self.assertEqual(meal_plan.date, date.today())
        self.assertEqual(meal_plan.meal_type, MealType.BREAKFAST.value)
        self.assertEqual(len(meal_plan.recipes), 0)
    
    def test_recipe_creation(self):
        """Test creating a Recipe."""
        recipe = Recipe(
            name="オムレツ",
            description="シンプルなオムレツのレシピ",
            preparation_time=15,
            cooking_instructions="1. 卵を溶く\n2. フライパンで焼く",
            category=RecipeCategory.MAIN_DISH.value,
        )
        
        self.assertEqual(recipe.name, "オムレツ")
        self.assertEqual(recipe.description, "シンプルなオムレツのレシピ")
        self.assertEqual(recipe.preparation_time, 15)
        self.assertEqual(recipe.cooking_instructions, "1. 卵を溶く\n2. フライパンで焼く")
        self.assertEqual(recipe.category, RecipeCategory.MAIN_DISH.value)
        self.assertEqual(len(recipe.ingredients), 0)
    
    def test_ingredient_creation(self):
        """Test creating an Ingredient."""
        recipe = Recipe(name="オムレツ")
        
        ingredient = Ingredient(
            recipe_id=1,
            name="卵",
            quantity=2,
            unit="個",
            category=IngredientCategory.OTHER.value,
        )
        
        self.assertEqual(ingredient.name, "卵")
        self.assertEqual(ingredient.quantity, 2)
        self.assertEqual(ingredient.unit, "個")
        self.assertEqual(ingredient.category, IngredientCategory.OTHER.value)
    
    def test_shopping_list_creation(self):
        """Test creating a ShoppingList."""
        today = date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        shopping_list = ShoppingList(
            name="週末の買い物",
            date_range_start=today,
            date_range_end=tomorrow,
        )
        
        self.assertEqual(shopping_list.name, "週末の買い物")
        self.assertEqual(shopping_list.date_range_start, today)
        self.assertEqual(shopping_list.date_range_end, tomorrow)
        self.assertEqual(len(shopping_list.items), 0)
    
    def test_shopping_list_item_creation(self):
        """Test creating a ShoppingListItem."""
        item = ShoppingListItem(
            shopping_list_id=1,
            ingredient_name="卵",
            total_quantity=6,
            unit="個",
            category=IngredientCategory.OTHER.value,
            is_purchased=False,
        )
        
        self.assertEqual(item.ingredient_name, "卵")
        self.assertEqual(item.total_quantity, 6)
        self.assertEqual(item.unit, "個")
        self.assertEqual(item.category, IngredientCategory.OTHER.value)
        self.assertEqual(item.is_purchased, False)
    
    def test_meal_plan_to_dict(self):
        """Test converting a MealPlan to a dictionary."""
        today = date.today()
        meal_plan = MealPlan(
            id=1,
            name="朝食メニュー",
            date=today,
            meal_type=MealType.BREAKFAST.value,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        
        meal_plan_dict = meal_plan.to_dict()
        
        self.assertEqual(meal_plan_dict["id"], 1)
        self.assertEqual(meal_plan_dict["name"], "朝食メニュー")
        self.assertEqual(meal_plan_dict["date"], today)
        self.assertEqual(meal_plan_dict["meal_type"], MealType.BREAKFAST.value)
        self.assertIn("created_at", meal_plan_dict)
        self.assertIn("updated_at", meal_plan_dict)


if __name__ == "__main__":
    unittest.main()