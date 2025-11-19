"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Sound Healing App Schemas

class HealingSession(BaseModel):
    """Logged meditation/sound healing session"""
    track_id: Optional[str] = Field(None, description="ID or code of track used")
    track_name: str = Field(..., description="Name of the sound/track")
    mode: str = Field(..., description="tone|audio|nature")
    duration_seconds: int = Field(..., ge=1, description="Planned or actual duration")
    mood_before: Optional[str] = Field(None, description="How you felt before")
    mood_after: Optional[str] = Field(None, description="How you felt after")
    notes: Optional[str] = Field(None, description="Optional notes")

class JournalEntry(BaseModel):
    """Short reflective journal entry"""
    text: str = Field(..., description="Journal text")
    tags: Optional[List[str]] = Field(default=None, description="Optional tags")
    created_at: Optional[datetime] = Field(default=None, description="Client timestamp if any")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
