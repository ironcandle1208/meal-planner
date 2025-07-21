"""
ShoppingList and ShoppingListItem models for the meal planner application.
"""

from datetime import date
from typing import List

from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from meals.models.base import BaseModel
from meals.models.enums import IngredientCategory


class ShoppingList(BaseModel):
    """ShoppingList model."""
    
    __tablename__ = "shopping_lists"
    
    name = Column(String, nullable=False)
    date_range_start = Column(Date, nullable=False)
    date_range_end = Column(Date, nullable=False)
    
    # Relationships
    items = relationship("ShoppingListItem", back_populates="shopping_list", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """String representation of the ShoppingList."""
        return f"<ShoppingList(id={self.id}, name='{self.name}', date_range='{self.date_range_start} to {self.date_range_end}')>"


class ShoppingListItem(BaseModel):
    """ShoppingListItem model."""
    
    __tablename__ = "shopping_list_items"
    
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id", ondelete="CASCADE"), nullable=False)
    ingredient_name = Column(String, nullable=False)
    total_quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    category = Column(String, nullable=True)
    is_purchased = Column(Boolean, default=False)
    
    # Relationships
    shopping_list = relationship("ShoppingList", back_populates="items")
    
    def __repr__(self) -> str:
        """String representation of the ShoppingListItem."""
        return f"<ShoppingListItem(id={self.id}, ingredient_name='{self.ingredient_name}', total_quantity={self.total_quantity}, unit='{self.unit}', is_purchased={self.is_purchased})>"