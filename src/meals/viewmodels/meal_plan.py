"""
MealPlan ViewModel for the meal planner application.
"""

from datetime import date
from typing import Dict, List, Optional, Union

from meals.models.enums import MealType
from meals.repositories.meal_plan import MealPlanRepository
from meals.repositories.recipe import RecipeRepository
from meals.schemas.meal_plan import MealPlanCreate, MealPlanRead, MealPlanUpdate
from meals.schemas.recipe import RecipeRead
from meals.utils.exceptions import DatabaseException, ValidationException
from meals.viewmodels.base import BaseViewModel


class MealPlanViewModel(BaseViewModel):
    """ViewModel for MealPlan model."""
    
    def __init__(self):
        """Initialize the ViewModel."""
        super().__init__()
        self.meal_plan_repo = MealPlanRepository()
        self.recipe_repo = RecipeRepository()
    
    def create_meal_plan(self, data: Dict) -> Optional[MealPlanRead]:
        """Create a new meal plan."""
        try:
            # Validate required fields
            self.validate_required_fields(data, ["name", "date", "meal_type"])
            
            # Check if meal plan already exists for this date and meal type
            existing = self.meal_plan_repo.get_by_date_and_meal_type(
                date_val=data["date"],
                meal_type=data["meal_type"],
            )
            if existing:
                raise ValidationException(
                    f"A meal plan already exists for {data['date']} ({data['meal_type']})"
                )
            
            # Create meal plan schema
            recipe_ids = data.pop("recipe_ids", [])
            meal_plan_create = MealPlanCreate(**data)
            
            # Create meal plan
            meal_plan = self.meal_plan_repo.create(meal_plan_create.model_dump(exclude={"recipe_ids"}))
            
            # Add recipes if provided
            for recipe_id in recipe_ids:
                self.meal_plan_repo.add_recipe_to_meal_plan(meal_plan.id, recipe_id)
            
            # Get the created meal plan with recipes
            result = self.meal_plan_repo.get_with_recipes(meal_plan.id)
            
            # Convert to schema
            meal_plan_read = MealPlanRead.model_validate(result)
            
            # Handle success
            self._handle_success("create_meal_plan", meal_plan_read)
            
            return meal_plan_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("create_meal_plan", e)
            return None
    
    def update_meal_plan(self, meal_plan_id: int, data: Dict) -> Optional[MealPlanRead]:
        """Update a meal plan."""
        try:
            # Check if meal plan exists
            meal_plan = self.meal_plan_repo.get_by_id(meal_plan_id)
            if not meal_plan:
                raise ValidationException(f"Meal plan with ID {meal_plan_id} not found")
            
            # Check if date and meal type are being updated and if they would conflict
            if "date" in data and "meal_type" in data:
                existing = self.meal_plan_repo.get_by_date_and_meal_type(
                    date_val=data["date"],
                    meal_type=data["meal_type"],
                )
                if existing and existing.id != meal_plan_id:
                    raise ValidationException(
                        f"A meal plan already exists for {data['date']} ({data['meal_type']})"
                    )
            elif "date" in data:
                existing = self.meal_plan_repo.get_by_date_and_meal_type(
                    date_val=data["date"],
                    meal_type=meal_plan.meal_type,
                )
                if existing and existing.id != meal_plan_id:
                    raise ValidationException(
                        f"A meal plan already exists for {data['date']} ({meal_plan.meal_type})"
                    )
            elif "meal_type" in data:
                existing = self.meal_plan_repo.get_by_date_and_meal_type(
                    date_val=meal_plan.date,
                    meal_type=data["meal_type"],
                )
                if existing and existing.id != meal_plan_id:
                    raise ValidationException(
                        f"A meal plan already exists for {meal_plan.date} ({data['meal_type']})"
                    )
            
            # Handle recipe IDs separately
            recipe_ids = data.pop("recipe_ids", None)
            
            # Create update schema
            meal_plan_update = MealPlanUpdate(**data)
            
            # Update meal plan
            updated_meal_plan = self.meal_plan_repo.update(
                meal_plan_id, meal_plan_update.model_dump(exclude_none=True)
            )
            
            # Update recipes if provided
            if recipe_ids is not None:
                # Get current recipes
                meal_plan_with_recipes = self.meal_plan_repo.get_with_recipes(meal_plan_id)
                current_recipe_ids = [recipe.id for recipe in meal_plan_with_recipes.recipes]
                
                # Remove recipes that are not in the new list
                for recipe_id in current_recipe_ids:
                    if recipe_id not in recipe_ids:
                        self.meal_plan_repo.remove_recipe_from_meal_plan(meal_plan_id, recipe_id)
                
                # Add recipes that are not already in the meal plan
                for recipe_id in recipe_ids:
                    if recipe_id not in current_recipe_ids:
                        self.meal_plan_repo.add_recipe_to_meal_plan(meal_plan_id, recipe_id)
            
            # Get the updated meal plan with recipes
            result = self.meal_plan_repo.get_with_recipes(meal_plan_id)
            
            # Convert to schema
            meal_plan_read = MealPlanRead.model_validate(result)
            
            # Handle success
            self._handle_success("update_meal_plan", meal_plan_read)
            
            return meal_plan_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("update_meal_plan", e)
            return None
    
    def delete_meal_plan(self, meal_plan_id: int) -> bool:
        """Delete a meal plan."""
        try:
            # Check if meal plan exists
            meal_plan = self.meal_plan_repo.get_by_id(meal_plan_id)
            if not meal_plan:
                raise ValidationException(f"Meal plan with ID {meal_plan_id} not found")
            
            # Delete meal plan
            result = self.meal_plan_repo.delete(meal_plan_id)
            
            # Handle success
            self._handle_success("delete_meal_plan", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("delete_meal_plan", e)
            return False
    
    def get_meal_plan(self, meal_plan_id: int) -> Optional[MealPlanRead]:
        """Get a meal plan by ID."""
        try:
            # Get meal plan with recipes
            meal_plan = self.meal_plan_repo.get_with_recipes(meal_plan_id)
            if not meal_plan:
                return None
            
            # Convert to schema
            meal_plan_read = MealPlanRead.model_validate(meal_plan)
            
            return meal_plan_read
        except DatabaseException as e:
            self._handle_error("get_meal_plan", e)
            return None
    
    def get_all_meal_plans(self) -> List[MealPlanRead]:
        """Get all meal plans."""
        try:
            # Get all meal plans with recipes
            meal_plans = self.meal_plan_repo.get_all_with_recipes()
            
            # Convert to schemas
            meal_plan_reads = [MealPlanRead.model_validate(mp) for mp in meal_plans]
            
            return meal_plan_reads
        except DatabaseException as e:
            self._handle_error("get_all_meal_plans", e)
            return []
    
    def get_meal_plans_by_date_range(self, start_date: date, end_date: date) -> List[MealPlanRead]:
        """Get meal plans by date range."""
        try:
            # Get meal plans by date range
            meal_plans = self.meal_plan_repo.get_by_date_range(start_date, end_date)
            
            # Convert to schemas
            meal_plan_reads = [MealPlanRead.model_validate(mp) for mp in meal_plans]
            
            return meal_plan_reads
        except DatabaseException as e:
            self._handle_error("get_meal_plans_by_date_range", e)
            return []
    
    def get_meal_plan_by_date_and_meal_type(self, date_val: date, meal_type: MealType) -> Optional[MealPlanRead]:
        """Get a meal plan by date and meal type."""
        try:
            # Get meal plan by date and meal type
            meal_plan = self.meal_plan_repo.get_by_date_and_meal_type(date_val, meal_type)
            if not meal_plan:
                return None
            
            # Convert to schema
            meal_plan_read = MealPlanRead.model_validate(meal_plan)
            
            return meal_plan_read
        except DatabaseException as e:
            self._handle_error("get_meal_plan_by_date_and_meal_type", e)
            return None
    
    def add_recipe_to_meal_plan(self, meal_plan_id: int, recipe_id: int) -> bool:
        """Add a recipe to a meal plan."""
        try:
            # Check if meal plan exists
            meal_plan = self.meal_plan_repo.get_by_id(meal_plan_id)
            if not meal_plan:
                raise ValidationException(f"Meal plan with ID {meal_plan_id} not found")
            
            # Check if recipe exists
            recipe = self.recipe_repo.get_by_id(recipe_id)
            if not recipe:
                raise ValidationException(f"Recipe with ID {recipe_id} not found")
            
            # Add recipe to meal plan
            result = self.meal_plan_repo.add_recipe_to_meal_plan(meal_plan_id, recipe_id)
            
            # Handle success
            self._handle_success("add_recipe_to_meal_plan", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("add_recipe_to_meal_plan", e)
            return False
    
    def remove_recipe_from_meal_plan(self, meal_plan_id: int, recipe_id: int) -> bool:
        """Remove a recipe from a meal plan."""
        try:
            # Check if meal plan exists
            meal_plan = self.meal_plan_repo.get_by_id(meal_plan_id)
            if not meal_plan:
                raise ValidationException(f"Meal plan with ID {meal_plan_id} not found")
            
            # Remove recipe from meal plan
            result = self.meal_plan_repo.remove_recipe_from_meal_plan(meal_plan_id, recipe_id)
            
            # Handle success
            self._handle_success("remove_recipe_from_meal_plan", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("remove_recipe_from_meal_plan", e)
            return False