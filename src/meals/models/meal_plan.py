"""
MealPlan model for the meal planner application.
"""

from datetime import date
from typing import List

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from meals.models.base import Base, BaseModel
from meals.models.enums import MealType

# Association table for many-to-many relationship between MealPlan and Recipe
meal_plan_recipes = Table(
    "meal_plan_recipes",
    Base.metadata,
    Column("meal_plan_id", Integer, ForeignKey("meal_plans.id", ondelete="CASCADE"), primary_key=True),
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
)


class MealPlan(BaseModel):
    """MealPlan model."""
    
    __tablename__ = "meal_plans"
    __table_args__ = (UniqueConstraint("date", "meal_type", name="uq_meal_plan_date_type"),)
    
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String, nullable=False)
    
    # Relationships
    recipes = relationship("Recipe", secondary=meal_plan_recipes, back_populates="meal_plans")
    
    def __repr__(self) -> str:
        """String representation of the MealPlan."""
        return f"<MealPlan(id={self.id}, name='{self.name}', date='{self.date}', meal_type='{self.meal_type}')>"