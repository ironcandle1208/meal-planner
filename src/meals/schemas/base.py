"""
Base schema for Pydantic models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for all Pydantic models."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None