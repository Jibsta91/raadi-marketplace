from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Message schemas
class MessageBase(BaseModel):
    subject: Optional[str] = None
    content: str
    listing_id: Optional[int] = None
    thread_id: Optional[str] = None


class MessageCreate(MessageBase):
    recipient_id: int


class MessageResponse(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    is_read: bool
    is_archived: bool
    is_spam: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Favorite schemas
class FavoriteBase(BaseModel):
    pass


class FavoriteCreate(FavoriteBase):
    listing_id: int


class FavoriteResponse(FavoriteBase):
    id: int
    user_id: int
    listing_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Review schemas
class ReviewBase(BaseModel):
    rating: int  # 1-5 stars
    comment: Optional[str] = None
    listing_id: Optional[int] = None


class ReviewCreate(ReviewBase):
    reviewed_user_id: int


class ReviewResponse(ReviewBase):
    id: int
    reviewer_id: int
    reviewed_user_id: int
    is_verified_purchase: bool
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True


# SavedSearch schemas
class SavedSearchBase(BaseModel):
    name: str
    search_query: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    filters: Optional[str] = None


class SavedSearchCreate(SavedSearchBase):
    email_alerts: bool = True
    push_alerts: bool = True


class SavedSearchResponse(SavedSearchBase):
    id: int
    user_id: int
    email_alerts: bool
    push_alerts: bool
    created_at: datetime
    last_checked: Optional[datetime] = None

    class Config:
        from_attributes = True
