"""
Tests for the repositories module.
"""

import datetime
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from meals.models import Base, Ingredient, MealPlan, Recipe, ShoppingList, ShoppingListItem
from meals.models.enums import IngredientCategory, MealType, RecipeCategory
from meals.repositories.meal_plan import MealPlanRepository
from meals.repositories.recipe import RecipeRepository
from meals.repositories.shopping_list import ShoppingListRepository


class TestRepositories(unittest.TestCase):
    """Tests for the repositories module."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create an in-memory SQLite database
        self.engine = create_engine("sqlite:///:memory:")
        
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
        
        # Add some test data
        self._add_test_data()
    
    def tearDown(self):
        """Clean up the test environment."""
        self.session.close()
    
    def _add_test_data(self):
        """Add test data to the database."""
        # Create recipes
        recipe1 = Recipe(
            name="オムレツ",
            description="シンプルなオムレツのレシピ",
            preparation_time=15,
            cooking_instructions="1. 卵を溶く\n2. フライパンで焼く",
            category=RecipeCategory.MAIN_DISH.value,
        )
        
        recipe2 = Recipe(
            name="サラダ",
            description="シンプルなサラダのレシピ",
            preparation_time=10,
            cooking_instructions="1. 野菜を切る\n2. ドレッシングをかける",
            category=RecipeCategory.SALAD.value,
        )
        
        self.session.add(recipe1)
        self.session.add(recipe2)
        self.session.flush()
        
        # Create ingredients
        ingredient1 = Ingredient(
            recipe_id=recipe1.id,
            name="卵",
            quantity=2,
            unit="個",
            category=IngredientCategory.OTHER.value,
        )
        
        ingredient2 = Ingredient(
            recipe_id=recipe1.id,
            name="塩",
            quantity=1,
            unit="小さじ",
            category=IngredientCategory.CONDIMENT.value,
        )
        
        ingredient3 = Ingredient(
            recipe_id=recipe2.id,
            name="レタス",
            quantity=1,
            unit="個",
            category=IngredientCategory.VEGETABLE.value,
        )
        
        self.session.add(ingredient1)
        self.session.add(ingredient2)
        self.session.add(ingredient3)
        
        # Create meal plans
        today = date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        meal_plan1 = MealPlan(
            name="朝食メニュー",
            date=today,
            meal_type=MealType.BREAKFAST.value,
        )
        
        meal_plan2 = MealPlan(
            name="昼食メニュー",
            date=today,
            meal_type=MealType.LUNCH.value,
        )
        
        self.session.add(meal_plan1)
        self.session.add(meal_plan2)
        self.session.flush()
        
        # Add recipes to meal plans
        meal_plan1.recipes.append(recipe1)
        meal_plan2.recipes.append(recipe2)
        
        # Create shopping lists
        shopping_list = ShoppingList(
            name="週末の買い物",
            date_range_start=today,
            date_range_end=tomorrow,
        )
        
        self.session.add(shopping_list)
        self.session.flush()
        
        # Create shopping list items
        item1 = ShoppingListItem(
            shopping_list_id=shopping_list.id,
            ingredient_name="卵",
            total_quantity=6,
            unit="個",
            category=IngredientCategory.OTHER.value,
            is_purchased=False,
        )
        
        item2 = ShoppingListItem(
            shopping_list_id=shopping_list.id,
            ingredient_name="レタス",
            total_quantity=1,
            unit="個",
            category=IngredientCategory.VEGETABLE.value,
            is_purchased=True,
        )
        
        self.session.add(item1)
        self.session.add(item2)
        
        # Commit the changes
        self.session.commit()
    
    def test_meal_plan_repository_get_all(self):
        """Test getting all meal plans."""
        meal_plans = self.meal_plan_repo.get_all()
        
        self.assertEqual(len(meal_plans), 2)
        self.assertEqual(meal_plans[0].name, "朝食メニュー")
        self.assertEqual(meal_plans[1].name, "昼食メニュー")
    
    def test_meal_plan_repository_get_by_id(self):
        """Test getting a meal plan by ID."""
        meal_plan = self.meal_plan_repo.get_by_id(1)
        
        self.assertIsNotNone(meal_plan)
        self.assertEqual(meal_plan.name, "朝食メニュー")
    
    def test_meal_plan_repository_get_by_date_and_meal_type(self):
        """Test getting a meal plan by date and meal type."""
        today = date.today()
        meal_plan = self.meal_plan_repo.get_by_date_and_meal_type(today, MealType.BREAKFAST.value)
        
        self.assertIsNotNone(meal_plan)
        self.assertEqual(meal_plan.name, "朝食メニュー")
    
    def test_recipe_repository_get_all(self):
        """Test getting all recipes."""
        recipes = self.recipe_repo.get_all()
        
        self.assertEqual(len(recipes), 2)
        self.assertEqual(recipes[0].name, "オムレツ")
        self.assertEqual(recipes[1].name, "サラダ")
    
    def test_recipe_repository_get_by_id(self):
        """Test getting a recipe by ID."""
        recipe = self.recipe_repo.get_by_id(1)
        
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, "オムレツ")
    
    def test_recipe_repository_get_by_category(self):
        """Test getting recipes by category."""
        recipes = self.recipe_repo.get_by_category(RecipeCategory.MAIN_DISH.value)
        
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].name, "オムレツ")
    
    def test_recipe_repository_search(self):
        """Test searching recipes."""
        recipes = self.recipe_repo.search("オムレツ")
        
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].name, "オムレツ")
    
    def test_shopping_list_repository_get_all(self):
        """Test getting all shopping lists."""
        shopping_lists = self.shopping_list_repo.get_all()
        
        self.assertEqual(len(shopping_lists), 1)
        self.assertEqual(shopping_lists[0].name, "週末の買い物")
    
    def test_shopping_list_repository_get_by_id(self):
        """Test getting a shopping list by ID."""
        shopping_list = self.shopping_list_repo.get_by_id(1)
        
        self.assertIsNotNone(shopping_list)
        self.assertEqual(shopping_list.name, "週末の買い物")
    
    def test_shopping_list_repository_get_items_by_purchase_status(self):
        """Test getting shopping list items by purchase status."""
        items = self.shopping_list_repo.get_items_by_purchase_status(1, True)
        
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].ingredient_name, "レタス")


if __name__ == "__main__":
    unittest.main()