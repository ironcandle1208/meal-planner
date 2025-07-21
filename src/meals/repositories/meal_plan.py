"""
MealPlan repository for the meal planner application.
"""

from datetime import date
from typing import List, Optional, Type

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from meals.models import MealPlan, Recipe, meal_plan_recipes
from meals.models.enums import MealType
from meals.repositories.base import BaseRepository
from meals.utils.exceptions import DatabaseException


class MealPlanRepository(BaseRepository[MealPlan]):
    """Repository for MealPlan model."""
    
    @property
    def model_class(self) -> Type[MealPlan]:
        """Get the model class."""
        return MealPlan
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[MealPlan]:
        """Get meal plans by date range."""
        try:
            stmt = (
                select(MealPlan)
                .where(and_(MealPlan.date >= start_date, MealPlan.date <= end_date))
                .order_by(MealPlan.date, MealPlan.meal_type)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get meal plans by date range: {str(e)}")
    
    def get_by_date_and_meal_type(self, date_val: date, meal_type: MealType) -> Optional[MealPlan]:
        """Get meal plan by date and meal type."""
        try:
            stmt = (
                select(MealPlan)
                .where(and_(MealPlan.date == date_val, MealPlan.meal_type == meal_type))
                .options(joinedload(MealPlan.recipes))
            )
            return self.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get meal plan by date and meal type: {str(e)}")
    
    def add_recipe_to_meal_plan(self, meal_plan_id: int, recipe_id: int) -> bool:
        """Add a recipe to a meal plan."""
        try:
            meal_plan = self.get_by_id(meal_plan_id)
            if meal_plan is None:
                return False
            
            # Check if the recipe exists
            recipe = self.session.get(Recipe, recipe_id)
            if recipe is None:
                return False
            
            # Check if the recipe is already in the meal plan
            stmt = (
                select(meal_plan_recipes)
                .where(
                    and_(
                        meal_plan_recipes.c.meal_plan_id == meal_plan_id,
                        meal_plan_recipes.c.recipe_id == recipe_id,
                    )
                )
            )
            existing = self.session.execute(stmt).first()
            if existing is not None:
                return True  # Already exists
            
            # Add the recipe to the meal plan
            meal_plan.recipes.append(recipe)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to add recipe to meal plan: {str(e)}")
    
    def remove_recipe_from_meal_plan(self, meal_plan_id: int, recipe_id: int) -> bool:
        """Remove a recipe from a meal plan."""
        try:
            meal_plan = self.get_by_id(meal_plan_id)
            if meal_plan is None:
                return False
            
            # Check if the recipe exists
            recipe = self.session.get(Recipe, recipe_id)
            if recipe is None:
                return False
            
            # Remove the recipe from the meal plan
            if recipe in meal_plan.recipes:
                meal_plan.recipes.remove(recipe)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to remove recipe from meal plan: {str(e)}")
    
    def get_with_recipes(self, meal_plan_id: int) -> Optional[MealPlan]:
        """Get a meal plan with its recipes."""
        try:
            stmt = (
                select(MealPlan)
                .where(MealPlan.id == meal_plan_id)
                .options(joinedload(MealPlan.recipes))
            )
            return self.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get meal plan with recipes: {str(e)}")
    
    def get_all_with_recipes(self) -> List[MealPlan]:
        """Get all meal plans with their recipes."""
        try:
            stmt = select(MealPlan).options(joinedload(MealPlan.recipes))
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get all meal plans with recipes: {str(e)}")