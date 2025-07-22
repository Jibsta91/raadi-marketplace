from sqlalchemy import (Column, Integer, String, DateTime, Text, 
                        ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    
    # Message thread
    thread_id = Column(String, nullable=True, index=True)
    parent_message_id = Column(Integer, ForeignKey("messages.id"), 
                               nullable=True)
    
    # Participants
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Related listing
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    is_spam = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], 
                         back_populates="messages_sent")
    recipient = relationship("User", foreign_keys=[recipient_id], 
                            back_populates="messages_received")
    listing = relationship("Listing", back_populates="messages")
    replies = relationship("Message", backref="parent")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorites")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    
    # Review participants
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Related listing/transaction
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=True)
    
    # Status
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reviewer = relationship("User", foreign_keys=[reviewer_id], 
                           back_populates="reviews_given")
    reviewed_user = relationship("User", foreign_keys=[reviewed_user_id], 
                                back_populates="reviews_received")
    listing = relationship("Listing", back_populates="reviews")


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    search_query = Column(String, nullable=True)
    category = Column(String, nullable=True)
    location = Column(String, nullable=True)
    min_price = Column(Integer, nullable=True)
    max_price = Column(Integer, nullable=True)
    filters = Column(Text, nullable=True)  # JSON string of additional filters
    
    # User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification settings
    email_alerts = Column(Boolean, default=True)
    push_alerts = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_checked = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="saved_searches")
