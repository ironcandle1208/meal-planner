"""
Recipe and Ingredient models for the meal planner application.
"""

from typing import List

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from meals.models.base import BaseModel
from meals.models.enums import IngredientCategory, RecipeCategory
from meals.models.meal_plan import meal_plan_recipes


class Recipe(BaseModel):
    """Recipe model."""
    
    __tablename__ = "recipes"
    
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    preparation_time = Column(Integer, nullable=True)  # in minutes
    cooking_instructions = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    
    # Relationships
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", secondary=meal_plan_recipes, back_populates="recipes")
    
    def __repr__(self) -> str:
        """String representation of the Recipe."""
        return f"<Recipe(id={self.id}, name='{self.name}', category='{self.category}')>"


class Ingredient(BaseModel):
    """Ingredient model."""
    
    __tablename__ = "ingredients"
    
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    category = Column(String, nullable=True)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    
    def __repr__(self) -> str:
        """String representation of the Ingredient."""
        return f"<Ingredient(id={self.id}, name='{self.name}', quantity={self.quantity}, unit='{self.unit}')>"