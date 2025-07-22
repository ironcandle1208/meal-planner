"""
Tests for the viewmodels module.
"""

import datetime
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from meals.models.enums import MealType, RecipeCategory
from meals.viewmodels.meal_plan import MealPlanViewModel
from meals.viewmodels.recipe import RecipeViewModel
from meals.viewmodels.shopping_list import ShoppingListViewModel


class TestViewModels(unittest.TestCase):
    """Tests for the viewmodels module."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create mock repositories
        self.meal_plan_repo_patcher = patch("meals.viewmodels.meal_plan.MealPlanRepository")
        self.recipe_repo_patcher = patch("meals.viewmodels.recipe.RecipeRepository")
        self.shopping_list_repo_patcher = patch("meals.viewmodels.shopping_list.ShoppingListRepository")
        
        self.mock_meal_plan_repo = self.meal_plan_repo_patcher.start()
        self.mock_recipe_repo = self.recipe_repo_patcher.start()
        self.mock_shopping_list_repo = self.shopping_list_repo_patcher.start()
        
        # Create viewmodels
        self.meal_plan_vm = MealPlanViewModel()
        self.recipe_vm = RecipeViewModel()
        self.shopping_list_vm = ShoppingListViewModel()
    
    def tearDown(self):
        """Clean up the test environment."""
        self.meal_plan_repo_patcher.stop()
        self.recipe_repo_patcher.stop()
        self.shopping_list_repo_patcher.stop()
    
    def test_meal_plan_viewmodel_create_meal_plan(self):
        """Test creating a meal plan."""
        # Set up mock
        self.meal_plan_vm.meal_plan_repo.get_by_date_and_meal_type.return_value = None
        self.meal_plan_vm.meal_plan_repo.create.return_value = MagicMock(id=1)
        self.meal_plan_vm.meal_plan_repo.get_with_recipes.return_value = MagicMock(
            id=1,
            name="朝食メニュー",
            date=date.today(),
            meal_type=MealType.BREAKFAST.value,
            recipes=[],
        )
        
        # Register success handler
        success_handler = MagicMock()
        self.meal_plan_vm.register_success_handler("create_meal_plan", success_handler)
        
        # Create meal plan
        meal_plan_data = {
            "name": "朝食メニュー",
            "date": date.today(),
            "meal_type": MealType.BREAKFAST.value,
        }
        
        result = self.meal_plan_vm.create_meal_plan(meal_plan_data)
        
        # Check result
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "朝食メニュー")
        
        # Check if success handler was called
        success_handler.assert_called_once()
    
    def test_meal_plan_viewmodel_create_meal_plan_duplicate(self):
        """Test creating a duplicate meal plan."""
        # Set up mock
        self.meal_plan_vm.meal_plan_repo.get_by_date_and_meal_type.return_value = MagicMock()
        
        # Register error handler
        error_handler = MagicMock()
        self.meal_plan_vm.register_error_handler("create_meal_plan", error_handler)
        
        # Create meal plan
        meal_plan_data = {
            "name": "朝食メニュー",
            "date": date.today(),
            "meal_type": MealType.BREAKFAST.value,
        }
        
        result = self.meal_plan_vm.create_meal_plan(meal_plan_data)
        
        # Check result
        self.assertIsNone(result)
        
        # Check if error handler was called
        error_handler.assert_called_once()
    
    def test_recipe_viewmodel_create_recipe(self):
        """Test creating a recipe."""
        # Set up mock
        self.recipe_vm.recipe_repo.create_with_ingredients.return_value = MagicMock(id=1)
        self.recipe_vm.recipe_repo.get_with_ingredients.return_value = MagicMock(
            id=1,
            name="オムレツ",
            description="シンプルなオムレツのレシピ",
            preparation_time=15,
            cooking_instructions="1. 卵を溶く\n2. フライパンで焼く",
            category=RecipeCategory.MAIN_DISH.value,
            ingredients=[],
        )
        
        # Register success handler
        success_handler = MagicMock()
        self.recipe_vm.register_success_handler("create_recipe", success_handler)
        
        # Create recipe
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
            },
        ]
        
        result = self.recipe_vm.create_recipe(recipe_data, ingredients_data)
        
        # Check result
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "オムレツ")
        
        # Check if success handler was called
        success_handler.assert_called_once()
    
    def test_shopping_list_viewmodel_create_shopping_list(self):
        """Test creating a shopping list."""
        # Set up mock
        self.shopping_list_vm.shopping_list_repo.create.return_value = MagicMock(id=1)
        self.shopping_list_vm.shopping_list_repo.get_with_items.return_value = MagicMock(
            id=1,
            name="週末の買い物",
            date_range_start=date.today(),
            date_range_end=date.today() + datetime.timedelta(days=1),
            items=[],
        )
        
        # Register success handler
        success_handler = MagicMock()
        self.shopping_list_vm.register_success_handler("create_shopping_list", success_handler)
        
        # Create shopping list
        shopping_list_data = {
            "name": "週末の買い物",
            "date_range_start": date.today(),
            "date_range_end": date.today() + datetime.timedelta(days=1),
        }
        
        result = self.shopping_list_vm.create_shopping_list(shopping_list_data)
        
        # Check result
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "週末の買い物")
        
        # Check if success handler was called
        success_handler.assert_called_once()
    
    def test_shopping_list_viewmodel_create_shopping_list_invalid_date_range(self):
        """Test creating a shopping list with an invalid date range."""
        # Register error handler
        error_handler = MagicMock()
        self.shopping_list_vm.register_error_handler("create_shopping_list", error_handler)
        
        # Create shopping list
        shopping_list_data = {
            "name": "週末の買い物",
            "date_range_start": date.today() + datetime.timedelta(days=1),
            "date_range_end": date.today(),
        }
        
        result = self.shopping_list_vm.create_shopping_list(shopping_list_data)
        
        # Check result
        self.assertIsNone(result)
        
        # Check if error handler was called
        error_handler.assert_called_once()


if __name__ == "__main__":
    unittest.main()