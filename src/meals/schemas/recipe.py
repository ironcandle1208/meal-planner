"""
Schemas for Recipe and Ingredient models.
"""

from typing import List, Optional

from pydantic import Field, field_validator

from meals.models.enums import IngredientCategory, RecipeCategory
from meals.schemas.base import BaseSchema


class IngredientBase(BaseSchema):
    """Base schema for Ingredient."""
    
    name: str
    quantity: float
    unit: str
    category: Optional[IngredientCategory] = None
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        """Validate category is a valid IngredientCategory."""
        if v is None:
            return None
        if isinstance(v, str):
            return IngredientCategory(v)
        return v


class IngredientCreate(IngredientBase):
    """Schema for creating an Ingredient."""
    
    recipe_id: Optional[int] = None


class IngredientRead(IngredientBase):
    """Schema for reading an Ingredient."""
    
    id: int
    recipe_id: int


class RecipeBase(BaseSchema):
    """Base schema for Recipe."""
    
    name: str
    description: Optional[str] = None
    preparation_time: Optional[int] = None
    cooking_instructions: Optional[str] = None
    category: Optional[RecipeCategory] = None
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        """Validate category is a valid RecipeCategory."""
        if v is None:
            return None
        if isinstance(v, str):
            return RecipeCategory(v)
        return v


class RecipeCreate(RecipeBase):
    """Schema for creating a Recipe."""
    
    ingredients: Optional[List[IngredientCreate]] = Field(default_factory=list)


class RecipeRead(RecipeBase):
    """Schema for reading a Recipe."""
    
    id: int
    ingredients: Optional[List[IngredientRead]] = None
    
    # These will be populated when relationships are loaded
    meal_plans: Optional[List["MealPlanRead"]] = None


class RecipeUpdate(BaseSchema):
    """Schema for updating a Recipe."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    preparation_time: Optional[int] = None
    cooking_instructions: Optional[str] = None
    category: Optional[RecipeCategory] = None
    ingredients: Optional[List[IngredientCreate]] = None


# Avoid circular imports
from meals.schemas.meal_plan import MealPlanRead  # noqa
RecipeRead.model_rebuild()