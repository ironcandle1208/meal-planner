"""
Schemas for ShoppingList and ShoppingListItem models.
"""

from datetime import date
from typing import List, Optional

from pydantic import Field, field_validator

from meals.models.enums import IngredientCategory
from meals.schemas.base import BaseSchema


class ShoppingListItemBase(BaseSchema):
    """Base schema for ShoppingListItem."""
    
    ingredient_name: str
    total_quantity: float
    unit: str
    category: Optional[IngredientCategory] = None
    is_purchased: bool = False
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        """Validate category is a valid IngredientCategory."""
        if v is None:
            return None
        if isinstance(v, str):
            return IngredientCategory(v)
        return v


class ShoppingListItemCreate(ShoppingListItemBase):
    """Schema for creating a ShoppingListItem."""
    
    shopping_list_id: Optional[int] = None


class ShoppingListItemRead(ShoppingListItemBase):
    """Schema for reading a ShoppingListItem."""
    
    id: int
    shopping_list_id: int


class ShoppingListItemUpdate(BaseSchema):
    """Schema for updating a ShoppingListItem."""
    
    ingredient_name: Optional[str] = None
    total_quantity: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[IngredientCategory] = None
    is_purchased: Optional[bool] = None


class ShoppingListBase(BaseSchema):
    """Base schema for ShoppingList."""
    
    name: str
    date_range_start: date
    date_range_end: date


class ShoppingListCreate(ShoppingListBase):
    """Schema for creating a ShoppingList."""
    
    items: Optional[List[ShoppingListItemCreate]] = Field(default_factory=list)


class ShoppingListRead(ShoppingListBase):
    """Schema for reading a ShoppingList."""
    
    id: int
    items: Optional[List[ShoppingListItemRead]] = None


class ShoppingListUpdate(BaseSchema):
    """Schema for updating a ShoppingList."""
    
    name: Optional[str] = None
    date_range_start: Optional[date] = None
    date_range_end: Optional[date] = None
    items: Optional[List[ShoppingListItemCreate]] = None