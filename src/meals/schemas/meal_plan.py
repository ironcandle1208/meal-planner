"""
Schemas for MealPlan model.
"""

from datetime import date
from typing import List, Optional

from pydantic import Field, field_validator

from meals.models.enums import MealType
from meals.schemas.base import BaseSchema


class MealPlanBase(BaseSchema):
    """Base schema for MealPlan."""
    
    name: str
    date: date
    meal_type: MealType
    
    @field_validator("meal_type")
    @classmethod
    def validate_meal_type(cls, v):
        """Validate meal_type is a valid MealType."""
        if isinstance(v, str):
            return MealType(v)
        return v


class MealPlanCreate(MealPlanBase):
    """Schema for creating a MealPlan."""
    
    recipe_ids: Optional[List[int]] = Field(default_factory=list)


class MealPlanRead(MealPlanBase):
    """Schema for reading a MealPlan."""
    
    id: int
    
    # These will be populated when relationships are loaded
    recipes: Optional[List["RecipeRead"]] = None


class MealPlanUpdate(BaseSchema):
    """Schema for updating a MealPlan."""
    
    name: Optional[str] = None
    date: Optional[date] = None
    meal_type: Optional[MealType] = None
    recipe_ids: Optional[List[int]] = None


# Avoid circular imports
from meals.schemas.recipe import RecipeRead  # noqa
MealPlanRead.model_rebuild()