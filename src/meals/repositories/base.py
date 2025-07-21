"""
Base repository interface for the meal planner application.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from meals.models.base import BaseModel
from meals.utils.database import get_db_session
from meals.utils.exceptions import DatabaseException

# Type variable for the model
T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T], ABC):
    """Base repository interface for all repositories."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize the repository with a session."""
        self._session = session
    
    @property
    def session(self) -> Session:
        """Get the session."""
        if self._session is None:
            # Get a new session from the generator
            self._session = next(get_db_session())
        return self._session
    
    @property
    @abstractmethod
    def model_class(self) -> Type[T]:
        """Get the model class."""
        pass
    
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new record."""
        try:
            instance = self.model_class(**data)
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to create {self.model_class.__name__}: {str(e)}")
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a record by ID."""
        try:
            return self.session.get(self.model_class, id)
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get {self.model_class.__name__} by ID: {str(e)}")
    
    def get_all(self) -> List[T]:
        """Get all records."""
        try:
            stmt = select(self.model_class)
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get all {self.model_class.__name__}s: {str(e)}")
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update a record."""
        try:
            instance = self.get_by_id(id)
            if instance is None:
                return None
            
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            self.session.commit()
            self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to update {self.model_class.__name__}: {str(e)}")
    
    def delete(self, id: int) -> bool:
        """Delete a record."""
        try:
            instance = self.get_by_id(id)
            if instance is None:
                return False
            
            self.session.delete(instance)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseException(f"Failed to delete {self.model_class.__name__}: {str(e)}")
    
    def close(self) -> None:
        """Close the session."""
        if self._session is not None:
            self._session.close()
            self._session = None