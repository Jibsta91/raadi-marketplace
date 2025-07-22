from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_business = Column(Boolean, default=False)
    
    # Profile stats
    total_listings = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    listings = relationship("Listing", back_populates="seller")
    messages_sent = relationship("Message", foreign_keys="Message.sender_id", 
                                back_populates="sender")
    messages_received = relationship("Message", 
                                   foreign_keys="Message.recipient_id", 
                                   back_populates="recipient")
    favorites = relationship("Favorite", back_populates="user")
    reviews_given = relationship("Review", foreign_keys="Review.reviewer_id", 
                                back_populates="reviewer")
    reviews_received = relationship("Review", 
                                  foreign_keys="Review.reviewed_user_id", 
                                  back_populates="reviewed_user")
    saved_searches = relationship("SavedSearch", back_populates="user")
