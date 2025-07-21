"""
Recipe repository for the meal planner application.
"""

from typing import Dict, List, Optional, Type, Union

from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from meals.models import Ingredient, Recipe
from meals.models.enums import RecipeCategory
from meals.repositories.base import BaseRepository
from meals.utils.exceptions import DatabaseException


class RecipeRepository(BaseRepository[Recipe]):
    """Repository for Recipe model."""
    
    @property
    def model_class(self) -> Type[Recipe]:
        """Get the model class."""
        return Recipe
    
    def create_with_ingredients(self, recipe_data: Dict, ingredients_data: List[Dict]) -> Recipe:
        """Create a recipe with ingredients."""
        try:
            # Create the recipe
            recipe = Recipe(**recipe_data)
            self.session.add(recipe)
            self.session.flush()  # Flush to get the recipe ID
            
            # Create the ingredients
            for ingredient_data in ingredients_data:
                ingredient = Ingredient(recipe_id=recipe.id, **ingredient_data)
                self.session.add(ingredient)
            
            self.session.commit()
            self.session.refresh(recipe)
            return recipe
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to create recipe with ingredients: {str(e)}")
    
    def get_by_category(self, category: RecipeCategory) -> List[Recipe]:
        """Get recipes by category."""
        try:
            stmt = select(Recipe).where(Recipe.category == category)
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get recipes by category: {str(e)}")
    
    def search(self, query: str) -> List[Recipe]:
        """Search recipes by name or ingredients."""
        try:
            # Convert query to lowercase for case-insensitive search
            search_term = f"%{query.lower()}%"
            
            stmt = (
                select(Recipe)
                .distinct()
                .join(Recipe.ingredients, isouter=True)
                .where(
                    or_(
                        func.lower(Recipe.name).like(search_term),
                        func.lower(Recipe.description).like(search_term),
                        func.lower(Ingredient.name).like(search_term),
                    )
                )
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to search recipes: {str(e)}")
    
    def get_with_ingredients(self, recipe_id: int) -> Optional[Recipe]:
        """Get a recipe with its ingredients."""
        try:
            stmt = (
                select(Recipe)
                .where(Recipe.id == recipe_id)
                .options(joinedload(Recipe.ingredients))
            )
            return self.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get recipe with ingredients: {str(e)}")
    
    def get_all_with_ingredients(self) -> List[Recipe]:
        """Get all recipes with their ingredients."""
        try:
            stmt = select(Recipe).options(joinedload(Recipe.ingredients))
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get all recipes with ingredients: {str(e)}")
    
    def update_with_ingredients(
        self, recipe_id: int, recipe_data: Dict, ingredients_data: Optional[List[Dict]] = None
    ) -> Optional[Recipe]:
        """Update a recipe with ingredients."""
        try:
            # Get the recipe
            recipe = self.get_by_id(recipe_id)
            if recipe is None:
                return None
            
            # Update recipe fields
            for key, value in recipe_data.items():
                if hasattr(recipe, key):
                    setattr(recipe, key, value)
            
            # Update ingredients if provided
            if ingredients_data is not None:
                # Delete existing ingredients
                self.session.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).delete()
                
                # Create new ingredients
                for ingredient_data in ingredients_data:
                    ingredient = Ingredient(recipe_id=recipe_id, **ingredient_data)
                    self.session.add(ingredient)
            
            self.session.commit()
            self.session.refresh(recipe)
            return recipe
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to update recipe with ingredients: {str(e)}")
    
    def add_ingredient(self, recipe_id: int, ingredient_data: Dict) -> Optional[Ingredient]:
        """Add an ingredient to a recipe."""
        try:
            # Check if the recipe exists
            recipe = self.get_by_id(recipe_id)
            if recipe is None:
                return None
            
            # Create the ingredient
            ingredient = Ingredient(recipe_id=recipe_id, **ingredient_data)
            self.session.add(ingredient)
            self.session.commit()
            self.session.refresh(ingredient)
            return ingredient
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to add ingredient to recipe: {str(e)}")
    
    def remove_ingredient(self, ingredient_id: int) -> bool:
        """Remove an ingredient from a recipe."""
        try:
            # Check if the ingredient exists
            ingredient = self.session.get(Ingredient, ingredient_id)
            if ingredient is None:
                return False
            
            # Delete the ingredient
            self.session.delete(ingredient)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to remove ingredient from recipe: {str(e)}")
    
    def update_ingredient(self, ingredient_id: int, ingredient_data: Dict) -> Optional[Ingredient]:
        """Update an ingredient."""
        try:
            # Check if the ingredient exists
            ingredient = self.session.get(Ingredient, ingredient_id)
            if ingredient is None:
                return None
            
            # Update ingredient fields
            for key, value in ingredient_data.items():
                if hasattr(ingredient, key):
                    setattr(ingredient, key, value)
            
            self.session.commit()
            self.session.refresh(ingredient)
            return ingredient
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to update ingredient: {str(e)}")