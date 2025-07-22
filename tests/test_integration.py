"""
Integration tests for the meal planner application.
"""

import datetime
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from meals.models import Base, Ingredient, MealPlan, Recipe, ShoppingList, ShoppingListItem
from meals.models.enums import IngredientCategory, MealType, RecipeCategory
from meals.repositories.meal_plan import MealPlanRepository
from meals.repositories.recipe import RecipeRepository
from meals.repositories.shopping_list import ShoppingListRepository
from meals.viewmodels.meal_plan import MealPlanViewModel
from meals.viewmodels.recipe import RecipeViewModel
from meals.viewmodels.shopping_list import ShoppingListViewModel


class TestIntegration(unittest.TestCase):
    """Integration tests for the meal planner application."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary database file
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db_file.close()
        
        # Create an SQLite database
        self.engine = create_engine(f"sqlite:///{self.temp_db_file.name}")
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        
        # Create a session factory
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create a session
        self.session = self.SessionLocal()
        
        # Create repositories
        self.meal_plan_repo = MealPlanRepository(self.session)
        self.recipe_repo = RecipeRepository(self.session)
        self.shopping_list_repo = ShoppingListRepository(self.session)
        
        # Create viewmodels
        self.meal_plan_vm = MealPlanViewModel()
        self.meal_plan_vm.meal_plan_repo = self.meal_plan_repo
        self.meal_plan_vm.recipe_repo = self.recipe_repo
        
        self.recipe_vm = RecipeViewModel()
        self.recipe_vm.recipe_repo = self.recipe_repo
        
        self.shopping_list_vm = ShoppingListViewModel()
        self.shopping_list_vm.shopping_list_repo = self.shopping_list_repo
        self.shopping_list_vm.meal_plan_repo = self.meal_plan_repo
    
    def tearDown(self):
        """Clean up the test environment."""
        self.session.close()
        
        # Remove the temporary database file
        os.unlink(self.temp_db_file.name)
    
    def test_create_recipe_and_meal_plan(self):
        """Test creating a recipe and a meal plan."""
        # Create a recipe
        recipe_data = {
            "name": "オムレツ",
            "description": "シンプルなオムレツのレシピ",
            "preparation_time": 15,
            "cooking_instructions": "1. 卵を溶く\n2. フライパンで焼く",
            "category": RecipeCategory.MAIN_DISH.value,
        }
        
        ingredients_data = [
            {
                "name": "卵",
                "quantity": 2,
                "unit": "個",
                "category": IngredientCategory.OTHER.value,
            },
            {
                "name": "塩",
                "quantity": 1,
                "unit": "小さじ",
                "category": IngredientCategory.CONDIMENT.value,
            },
        ]
        
        recipe = self.recipe_vm.create_recipe(recipe_data, ingredients_data)
        
        # Check if recipe was created
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, "オムレツ")
        self.assertEqual(len(recipe.ingredients), 2)
        
        # Create a meal plan
        meal_plan_data = {
            "name": "朝食メニュー",
            "date": date.today(),
            "meal_type": MealType.BREAKFAST.value,
            "recipe_ids": [recipe.id],
        }
        
        meal_plan = self.meal_plan_vm.create_meal_plan(meal_plan_data)
        
        # Check if meal plan was created
        self.assertIsNotNone(meal_plan)
        self.assertEqual(meal_plan.name, "朝食メニュー")
        self.assertEqual(len(meal_plan.recipes), 1)
        self.assertEqual(meal_plan.recipes[0].name, "オムレツ")
    
    def test_create_shopping_list_from_meal_plans(self):
        """Test creating a shopping list from meal plans."""
        # Create recipes
        recipe1_data = {
            "name": "オムレツ",
            "description": "シンプルなオムレツのレシピ",
            "preparation_time": 15,
            "cooking_instructions": "1. 卵を溶く\n2. フライパンで焼く",
            "category": RecipeCategory.MAIN_DISH.value,
        }
        
        recipe1_ingredients = [
            {
                "name": "卵",
                "quantity": 2,
                "unit": "個",
                "category": IngredientCategory.OTHER.value,
            },
            {
                "name": "塩",
                "quantity": 1,
                "unit": "小さじ",
                "category": IngredientCategory.CONDIMENT.value,
            },
        ]
        
        recipe1 = self.recipe_vm.create_recipe(recipe1_data, recipe1_ingredients)
        
        recipe2_data = {
            "name": "サラダ",
            "description": "シンプルなサラダのレシピ",
            "preparation_time": 10,
            "cooking_instructions": "1. 野菜を切る\n2. ドレッシングをかける",
            "category": RecipeCategory.SALAD.value,
        }
        
        recipe2_ingredients = [
            {
                "name": "レタス",
                "quantity": 1,
                "unit": "個",
                "category": IngredientCategory.VEGETABLE.value,
            },
            {
                "name": "トマト",
                "quantity": 2,
                "unit": "個",
                "category": IngredientCategory.VEGETABLE.value,
            },
        ]
        
        recipe2 = self.recipe_vm.create_recipe(recipe2_data, recipe2_ingredients)
        
        # Create meal plans
        today = date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        meal_plan1_data = {
            "name": "朝食メニュー",
            "date": today,
            "meal_type": MealType.BREAKFAST.value,
            "recipe_ids": [recipe1.id],
        }
        
        meal_plan1 = self.meal_plan_vm.create_meal_plan(meal_plan1_data)
        
        meal_plan2_data = {
            "name": "昼食メニュー",
            "date": today,
            "meal_type": MealType.LUNCH.value,
            "recipe_ids": [recipe2.id],
        }
        
        meal_plan2 = self.meal_plan_vm.create_meal_plan(meal_plan2_data)
        
        # Generate shopping list
        shopping_list = self.shopping_list_vm.generate_shopping_list_from_meal_plans(
            "週末の買い物", today, tomorrow
        )
        
        # Check if shopping list was created
        self.assertIsNotNone(shopping_list)
        self.assertEqual(shopping_list.name, "週末の買い物")
        self.assertEqual(len(shopping_list.items), 4)
        
        # Check if items were aggregated correctly
        egg_item = next((item for item in shopping_list.items if item.ingredient_name == "卵"), None)
        self.assertIsNotNone(egg_item)
        self.assertEqual(egg_item.total_quantity, 2)
        
        lettuce_item = next((item for item in shopping_list.items if item.ingredient_name == "レタス"), None)
        self.assertIsNotNone(lettuce_item)
        self.assertEqual(lettuce_item.total_quantity, 1)


if __name__ == "__main__":
    unittest.main()