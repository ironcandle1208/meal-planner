"""
ShoppingList repository for the meal planner application.
"""

from datetime import date
from typing import Dict, List, Optional, Type

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from meals.models import ShoppingList, ShoppingListItem
from meals.models.enums import IngredientCategory
from meals.repositories.base import BaseRepository
from meals.utils.exceptions import DatabaseException


class ShoppingListRepository(BaseRepository[ShoppingList]):
    """Repository for ShoppingList model."""
    
    @property
    def model_class(self) -> Type[ShoppingList]:
        """Get the model class."""
        return ShoppingList
    
    def create_with_items(self, shopping_list_data: Dict, items_data: List[Dict]) -> ShoppingList:
        """Create a shopping list with items."""
        try:
            # Create the shopping list
            shopping_list = ShoppingList(**shopping_list_data)
            self.session.add(shopping_list)
            self.session.flush()  # Flush to get the shopping list ID
            
            # Create the items
            for item_data in items_data:
                item = ShoppingListItem(shopping_list_id=shopping_list.id, **item_data)
                self.session.add(item)
            
            self.session.commit()
            self.session.refresh(shopping_list)
            return shopping_list
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to create shopping list with items: {str(e)}")
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[ShoppingList]:
        """Get shopping lists by date range."""
        try:
            stmt = (
                select(ShoppingList)
                .where(
                    and_(
                        ShoppingList.date_range_start <= end_date,
                        ShoppingList.date_range_end >= start_date,
                    )
                )
                .order_by(ShoppingList.date_range_start)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get shopping lists by date range: {str(e)}")
    
    def get_with_items(self, shopping_list_id: int) -> Optional[ShoppingList]:
        """Get a shopping list with its items."""
        try:
            stmt = (
                select(ShoppingList)
                .where(ShoppingList.id == shopping_list_id)
                .options(joinedload(ShoppingList.items))
            )
            return self.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get shopping list with items: {str(e)}")
    
    def get_all_with_items(self) -> List[ShoppingList]:
        """Get all shopping lists with their items."""
        try:
            stmt = select(ShoppingList).options(joinedload(ShoppingList.items))
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get all shopping lists with items: {str(e)}")
    
    def update_with_items(
        self, shopping_list_id: int, shopping_list_data: Dict, items_data: Optional[List[Dict]] = None
    ) -> Optional[ShoppingList]:
        """Update a shopping list with items."""
        try:
            # Get the shopping list
            shopping_list = self.get_by_id(shopping_list_id)
            if shopping_list is None:
                return None
            
            # Update shopping list fields
            for key, value in shopping_list_data.items():
                if hasattr(shopping_list, key):
                    setattr(shopping_list, key, value)
            
            # Update items if provided
            if items_data is not None:
                # Delete existing items
                self.session.query(ShoppingListItem).filter(
                    ShoppingListItem.shopping_list_id == shopping_list_id
                ).delete()
                
                # Create new items
                for item_data in items_data:
                    item = ShoppingListItem(shopping_list_id=shopping_list_id, **item_data)
                    self.session.add(item)
            
            self.session.commit()
            self.session.refresh(shopping_list)
            return shopping_list
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to update shopping list with items: {str(e)}")
    
    def add_item(self, shopping_list_id: int, item_data: Dict) -> Optional[ShoppingListItem]:
        """Add an item to a shopping list."""
        try:
            # Check if the shopping list exists
            shopping_list = self.get_by_id(shopping_list_id)
            if shopping_list is None:
                return None
            
            # Create the item
            item = ShoppingListItem(shopping_list_id=shopping_list_id, **item_data)
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to add item to shopping list: {str(e)}")
    
    def remove_item(self, item_id: int) -> bool:
        """Remove an item from a shopping list."""
        try:
            # Check if the item exists
            item = self.session.get(ShoppingListItem, item_id)
            if item is None:
                return False
            
            # Delete the item
            self.session.delete(item)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to remove item from shopping list: {str(e)}")
    
    def update_item(self, item_id: int, item_data: Dict) -> Optional[ShoppingListItem]:
        """Update an item."""
        try:
            # Check if the item exists
            item = self.session.get(ShoppingListItem, item_id)
            if item is None:
                return None
            
            # Update item fields
            for key, value in item_data.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            
            self.session.commit()
            self.session.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to update item: {str(e)}")
    
    def mark_item_as_purchased(self, item_id: int, is_purchased: bool = True) -> bool:
        """Mark an item as purchased or not purchased."""
        try:
            # Check if the item exists
            item = self.session.get(ShoppingListItem, item_id)
            if item is None:
                return False
            
            # Update the item
            item.is_purchased = is_purchased
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to mark item as purchased: {str(e)}")
    
    def get_items_by_category(self, shopping_list_id: int, category: IngredientCategory) -> List[ShoppingListItem]:
        """Get items by category."""
        try:
            stmt = (
                select(ShoppingListItem)
                .where(
                    and_(
                        ShoppingListItem.shopping_list_id == shopping_list_id,
                        ShoppingListItem.category == category,
                    )
                )
                .order_by(ShoppingListItem.ingredient_name)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get items by category: {str(e)}")
    
    def get_items_by_purchase_status(self, shopping_list_id: int, is_purchased: bool) -> List[ShoppingListItem]:
        """Get items by purchase status."""
        try:
            stmt = (
                select(ShoppingListItem)
                .where(
                    and_(
                        ShoppingListItem.shopping_list_id == shopping_list_id,
                        ShoppingListItem.is_purchased == is_purchased,
                    )
                )
                .order_by(ShoppingListItem.ingredient_name)
            )
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get items by purchase status: {str(e)}")