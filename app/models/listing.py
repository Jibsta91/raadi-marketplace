from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, Float, 
    ForeignKey, JSON, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.core.database import Base


class ListingStatus(PyEnum):
    ACTIVE = "active"
    SOLD = "sold"
    PAUSED = "paused"
    EXPIRED = "expired"
    DRAFT = "draft"


class ListingType(PyEnum):
    SELL = "sell"
    RENT = "rent"
    WANTED = "wanted"
    SERVICE = "service"
    JOB = "job"


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=True)  # Price in NOK øre
    price_type = Column(String, default="fixed")  # fixed, negotiable, from
    
    # Category and location
    category = Column(String, nullable=False, index=True)
    subcategory = Column(String, nullable=True)
    location = Column(String, nullable=False, index=True)
    postal_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Listing details
    listing_type = Column(Enum(ListingType), default=ListingType.SELL)
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE)
    condition = Column(String, nullable=True)  # new, used, defect
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    
    # Images and media
    image_urls = Column(JSON, default=list)
    main_image_url = Column(String, nullable=True)
    
    # Vehicle specific (for bil, mc, båt)
    kilometers = Column(Integer, nullable=True)
    fuel_type = Column(String, nullable=True)
    transmission = Column(String, nullable=True)
    engine_size = Column(String, nullable=True)
    horsepower = Column(Integer, nullable=True)
    
    # Real estate specific
    rooms = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    size_sqm = Column(Float, nullable=True)
    plot_size_sqm = Column(Float, nullable=True)
    property_type = Column(String, nullable=True)
    construction_year = Column(Integer, nullable=True)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    
    # Job specific
    job_type = Column(String, nullable=True)  # fulltime, parttime, freelance
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    company_name = Column(String, nullable=True)
    application_deadline = Column(DateTime, nullable=True)
    
    # Contact and seller info
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    seller_type = Column(String, default="private")  # private, business
    
    # Stats
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    message_count = Column(Integer, default=0)
    
    # Features and amenities
    features = Column(JSON, default=list)
    amenities = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime, nullable=True)
    sold_at = Column(DateTime, nullable=True)
    
    # Finn.no specific features
    is_featured = Column(Boolean, default=False)
    is_promoted = Column(Boolean, default=False)
    bump_count = Column(Integer, default=0)
    last_bumped = Column(DateTime, nullable=True)
    
    # Moderation
    is_approved = Column(Boolean, default=True)
    moderation_notes = Column(Text, nullable=True)
    
    # Relationships
    seller = relationship("User", back_populates="listings")
    messages = relationship("Message", back_populates="listing")
    favorites = relationship("Favorite", back_populates="listing")
    reviews = relationship("Review", back_populates="listing")
