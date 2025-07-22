from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.models.listing import ListingStatus, ListingType


# Base listing schema
class ListingBase(BaseModel):
    title: str
    description: str
    price: int
    category: str
    listing_type: Optional[str] = "sale"
    location: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: Optional[List[str]] = []
    
    # Vehicle specific
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    kilometers: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    
    # Real estate specific
    rooms: Optional[float] = None
    size_sqm: Optional[float] = None
    property_type: Optional[str] = None
    
    # Job specific
    salary: Optional[int] = None
    company: Optional[str] = None
    job_type: Optional[str] = None
    
    # Contact info
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    
    # Features
    features: Optional[List[str]] = []
    amenities: Optional[List[str]] = []


class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None
    images: Optional[List[str]] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    features: Optional[List[str]] = None
    amenities: Optional[List[str]] = None


class ListingResponse(ListingBase):
    id: int
    seller_id: int
    status: str
    view_count: int
    favorite_count: int
    message_count: int
    is_featured: bool
    is_promoted: bool
    bump_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_bumped: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    sold_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ListingSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    listing_type: Optional[str] = None
    
    # Vehicle filters
    make: Optional[str] = None
    max_kilometers: Optional[int] = None
    fuel_type: Optional[str] = None
    
    # Real estate filters
    min_rooms: Optional[float] = None
    max_rooms: Optional[float] = None
    min_size: Optional[float] = None
    property_type: Optional[str] = None
    
    # Job filters
    min_salary: Optional[int] = None
    company: Optional[str] = None
    job_type: Optional[str] = None
