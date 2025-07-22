"""
ShoppingList ViewModel for the meal planner application.
"""

from datetime import date
from typing import Dict, List, Optional, Tuple

from meals.models import Ingredient, MealPlan, Recipe
from meals.models.enums import IngredientCategory
from meals.repositories.meal_plan import MealPlanRepository
from meals.repositories.shopping_list import ShoppingListRepository
from meals.schemas.shopping_list import (
    ShoppingListCreate,
    ShoppingListItemCreate,
    ShoppingListItemRead,
    ShoppingListRead,
    ShoppingListUpdate,
)
from meals.utils.exceptions import DatabaseException, ValidationException
from meals.viewmodels.base import BaseViewModel


class ShoppingListViewModel(BaseViewModel):
    """ViewModel for ShoppingList model."""
    
    def __init__(self):
        """Initialize the ViewModel."""
        super().__init__()
        self.shopping_list_repo = ShoppingListRepository()
        self.meal_plan_repo = MealPlanRepository()
    
    def create_shopping_list(self, data: Dict, items_data: Optional[List[Dict]] = None) -> Optional[ShoppingListRead]:
        """Create a new shopping list."""
        try:
            # Validate required fields
            self.validate_required_fields(data, ["name", "date_range_start", "date_range_end"])
            
            # Validate date range
            if data["date_range_start"] > data["date_range_end"]:
                raise ValidationException("Start date must be before or equal to end date")
            
            # Create shopping list schema
            shopping_list_create = ShoppingListCreate(**data)
            
            # Create shopping list
            if items_data:
                # Validate required fields for each item
                for i, item_data in enumerate(items_data):
                    try:
                        self.validate_required_fields(
                            item_data, ["ingredient_name", "total_quantity", "unit"]
                        )
                    except ValidationException as e:
                        raise ValidationException(f"Item {i+1}: {str(e)}")
                
                # Create item schemas
                item_creates = [ShoppingListItemCreate(**item) for item in items_data]
                
                # Create shopping list with items
                shopping_list = self.shopping_list_repo.create_with_items(
                    shopping_list_create.model_dump(exclude={"items"}),
                    [item.model_dump() for item in item_creates],
                )
            else:
                # Create empty shopping list
                shopping_list = self.shopping_list_repo.create(
                    shopping_list_create.model_dump(exclude={"items"})
                )
            
            # Get the created shopping list with items
            result = self.shopping_list_repo.get_with_items(shopping_list.id)
            
            # Convert to schema
            shopping_list_read = ShoppingListRead.model_validate(result)
            
            # Handle success
            self._handle_success("create_shopping_list", shopping_list_read)
            
            return shopping_list_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("create_shopping_list", e)
            return None
    
    def update_shopping_list(
        self, shopping_list_id: int, data: Dict, items_data: Optional[List[Dict]] = None
    ) -> Optional[ShoppingListRead]:
        """Update a shopping list."""
        try:
            # Check if shopping list exists
            shopping_list = self.shopping_list_repo.get_by_id(shopping_list_id)
            if not shopping_list:
                raise ValidationException(f"Shopping list with ID {shopping_list_id} not found")
            
            # Validate date range if both dates are provided
            if "date_range_start" in data and "date_range_end" in data:
                if data["date_range_start"] > data["date_range_end"]:
                    raise ValidationException("Start date must be before or equal to end date")
            elif "date_range_start" in data:
                if data["date_range_start"] > shopping_list.date_range_end:
                    raise ValidationException("Start date must be before or equal to end date")
            elif "date_range_end" in data:
                if shopping_list.date_range_start > data["date_range_end"]:
                    raise ValidationException("Start date must be before or equal to end date")
            
            # Create update schema
            shopping_list_update = ShoppingListUpdate(**data)
            
            # Update shopping list
            if items_data is not None:
                # Validate required fields for each item
                for i, item_data in enumerate(items_data):
                    try:
                        self.validate_required_fields(
                            item_data, ["ingredient_name", "total_quantity", "unit"]
                        )
                    except ValidationException as e:
                        raise ValidationException(f"Item {i+1}: {str(e)}")
                
                # Create item schemas
                item_creates = [ShoppingListItemCreate(**item) for item in items_data]
                
                # Update shopping list with items
                updated_shopping_list = self.shopping_list_repo.update_with_items(
                    shopping_list_id,
                    shopping_list_update.model_dump(exclude_none=True, exclude={"items"}),
                    [item.model_dump() for item in item_creates],
                )
            else:
                # Update shopping list without changing items
                updated_shopping_list = self.shopping_list_repo.update(
                    shopping_list_id, shopping_list_update.model_dump(exclude_none=True, exclude={"items"})
                )
            
            # Get the updated shopping list with items
            result = self.shopping_list_repo.get_with_items(shopping_list_id)
            
            # Convert to schema
            shopping_list_read = ShoppingListRead.model_validate(result)
            
            # Handle success
            self._handle_success("update_shopping_list", shopping_list_read)
            
            return shopping_list_read
        except (ValidationException, DatabaseException) as e:
            self._handle_error("update_shopping_list", e)
            return None
    
    def delete_shopping_list(self, shopping_list_id: int) -> bool:
        """Delete a shopping list."""
        try:
            # Check if shopping list exists
            shopping_list = self.shopping_list_repo.get_by_id(shopping_list_id)
            if not shopping_list:
                raise ValidationException(f"Shopping list with ID {shopping_list_id} not found")
            
            # Delete shopping list
            result = self.shopping_list_repo.delete(shopping_list_id)
            
            # Handle success
            self._handle_success("delete_shopping_list", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("delete_shopping_list", e)
            return False
    
    def get_shopping_list(self, shopping_list_id: int) -> Optional[ShoppingListRead]:
        """Get a shopping list by ID."""
        try:
            # Get shopping list with items
            shopping_list = self.shopping_list_repo.get_with_items(shopping_list_id)
            if not shopping_list:
                return None
            
            # Convert to schema
            shopping_list_read = ShoppingListRead.model_validate(shopping_list)
            
            return shopping_list_read
        except DatabaseException as e:
            self._handle_error("get_shopping_list", e)
            return None
    
    def get_all_shopping_lists(self) -> List[ShoppingListRead]:
        """Get all shopping lists."""
        try:
            # Get all shopping lists with items
            shopping_lists = self.shopping_list_repo.get_all_with_items()
            
            # Convert to schemas
            shopping_list_reads = [ShoppingListRead.model_validate(sl) for sl in shopping_lists]
            
            return shopping_list_reads
        except DatabaseException as e:
            self._handle_error("get_all_shopping_lists", e)
            return []
    
    def get_shopping_lists_by_date_range(self, start_date: date, end_date: date) -> List[ShoppingListRead]:
        """Get shopping lists by date range."""
        try:
            # Get shopping lists by date range
            shopping_lists = self.shopping_list_repo.get_by_date_range(start_date, end_date)
            
            # Convert to schemas
            shopping_list_reads = [ShoppingListRead.model_validate(sl) for sl in shopping_lists]
            
            return shopping_list_reads
        except DatabaseException as e:
            self._handle_error("get_shopping_lists_by_date_range", e)
            return []
    
    def mark_item_as_purchased(self, item_id: int, is_purchased: bool = True) -> bool:
        """Mark an item as purchased or not purchased."""
        try:
            # Mark item as purchased
            result = self.shopping_list_repo.mark_item_as_purchased(item_id, is_purchased)
            if not result:
                raise ValidationException(f"Item with ID {item_id} not found")
            
            # Handle success
            self._handle_success("mark_item_as_purchased", result)
            
            return result
        except (ValidationException, DatabaseException) as e:
            self._handle_error("mark_item_as_purchased", e)
            return False
    
    def get_items_by_category(
        self, shopping_list_id: int, category: IngredientCategory
    ) -> List[ShoppingListItemRead]:
        """Get items by category."""
        try:
            # Check if shopping list exists
            shopping_list = self.shopping_list_repo.get_by_id(shopping_list_id)
            if not shopping_list:
                raise ValidationException(f"Shopping list with ID {shopping_list_id} not found")
            
            # Get items by category
            items = self.shopping_list_repo.get_items_by_category(shopping_list_id, category)
            
            # Convert to schemas
            item_reads = [ShoppingListItemRead.model_validate(item) for item in items]
            
            return item_reads
        except (ValidationException, DatabaseException) as e:
            self._handle_error("get_items_by_category", e)
            return []
    
    def get_items_by_purchase_status(
        self, shopping_list_id: int, is_purchased: bool
    ) -> List[ShoppingListItemRead]:
        """Get items by purchase status."""
        try:
            # Check if shopping list exists
            shopping_list = self.shopping_list_repo.get_by_id(shopping_list_id)
            if not shopping_list:
                raise ValidationException(f"Shopping list with ID {shopping_list_id} not found")
            
            # Get items by purchase status
            items = self.shopping_list_repo.get_items_by_purchase_status(shopping_list_id, is_purchased)
            
            # Convert to schemas
            item_reads = [ShoppingListItemRead.model_validate(item) for item in items]
            
            return item_reads
        except (ValidationException, DatabaseException) as e:
            self._handle_error("get_items_by_purchase_status", e)
            return []
    
    def generate_shopping_list_from_meal_plans(
        self, name: str, start_date: date, end_date: date
    ) -> Optional[ShoppingListRead]:
        """Generate a shopping list from meal plans in a date range."""
        try:
            # Validate date range
            if start_date > end_date:
                raise ValidationException("Start date must be before or equal to end date")
            
            # Get meal plans in the date range
            meal_plans = self.meal_plan_repo.get_by_date_range(start_date, end_date)
            if not meal_plans:
                raise ValidationException(f"No meal plans found between {start_date} and {end_date}")
            
            # Collect all ingredients from all recipes in all meal plans
            ingredients_map: Dict[Tuple[str, str, Optional[str]], float] = {}
            
            for meal_plan in meal_plans:
                # Load recipes for this meal plan
                meal_plan_with_recipes = self.meal_plan_repo.get_with_recipes(meal_plan.id)
                
                for recipe in meal_plan_with_recipes.recipes:
                    # Load ingredients for this recipe
                    recipe_with_ingredients = self.meal_plan_repo.session.query(Recipe).filter(
                        Recipe.id == recipe.id
                    ).first()
                    
                    for ingredient in recipe_with_ingredients.ingredients:
                        # Create a key for this ingredient (name, unit, category)
                        key = (ingredient.name, ingredient.unit, ingredient.category)
                        
                        # Add or update the quantity
                        if key in ingredients_map:
                            ingredients_map[key] += ingredient.quantity
                        else:
                            ingredients_map[key] = ingredient.quantity
            
            # Create shopping list items from the collected ingredients
            items_data = []
            for (name, unit, category), total_quantity in ingredients_map.items():
                items_data.append({
                    "ingredient_name": name,
                    "total_quantity": total_quantity,
                    "unit": unit,
                    "category": category,
                    "is_purchased": False,
                })
            
            # Create the shopping list
            shopping_list_data = {
                "name": name,
                "date_range_start": start_date,
                "date_range_end": end_date,
            }
            
            return self.create_shopping_list(shopping_list_data, items_data)
        except (ValidationException, DatabaseException) as e:
            self._handle_error("generate_shopping_list_from_meal_plans", e)
            return None