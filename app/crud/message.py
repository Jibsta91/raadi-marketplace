from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from app.models.message import Message, Favorite, Review, SavedSearch


# Message CRUD operations
def get_message(db: Session, message_id: int) -> Optional[Message]:
    """Get a message by ID."""
    return db.query(Message).filter(Message.id == message_id).first()


def get_user_messages(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Message]:
    """Get all messages for a user (sent and received)."""
    return (db.query(Message)
            .filter(or_(Message.sender_id == user_id, 
                       Message.recipient_id == user_id))
            .order_by(desc(Message.created_at))
            .offset(skip)
            .limit(limit)
            .all())


def get_conversation(
    db: Session,
    user1_id: int,
    user2_id: int,
    listing_id: Optional[int] = None
) -> List[Message]:
    """Get conversation between two users."""
    query = db.query(Message).filter(
        or_(
            and_(Message.sender_id == user1_id, 
                 Message.recipient_id == user2_id),
            and_(Message.sender_id == user2_id, 
                 Message.recipient_id == user1_id)
        )
    )
    
    if listing_id:
        query = query.filter(Message.listing_id == listing_id)
    
    return query.order_by(Message.created_at).all()


def create_message(
    db: Session,
    sender_id: int,
    recipient_id: int,
    content: str,
    subject: Optional[str] = None,
    listing_id: Optional[int] = None,
    thread_id: Optional[str] = None
) -> Message:
    """Create a new message."""
    db_message = Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content,
        subject=subject,
        listing_id=listing_id,
        thread_id=thread_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def mark_message_as_read(db: Session, message_id: int) -> Optional[Message]:
    """Mark a message as read."""
    from datetime import datetime
    
    db_message = get_message(db, message_id)
    if db_message:
        db_message.is_read = True
        db_message.read_at = datetime.utcnow()
        db.commit()
        db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int) -> bool:
    """Delete a message."""
    db_message = get_message(db, message_id)
    if not db_message:
        return False
    
    db.delete(db_message)
    db.commit()
    return True


# Favorite CRUD operations
def get_user_favorites(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Favorite]:
    """Get all favorites for a user."""
    return (db.query(Favorite)
            .filter(Favorite.user_id == user_id)
            .order_by(desc(Favorite.created_at))
            .offset(skip)
            .limit(limit)
            .all())


def is_favorite(db: Session, user_id: int, listing_id: int) -> bool:
    """Check if a listing is favorited by a user."""
    favorite = (db.query(Favorite)
                .filter(and_(Favorite.user_id == user_id, 
                           Favorite.listing_id == listing_id))
                .first())
    return favorite is not None


def add_favorite(db: Session, user_id: int, listing_id: int) -> Favorite:
    """Add a listing to favorites."""
    # Check if already favorited
    if is_favorite(db, user_id, listing_id):
        return None
    
    db_favorite = Favorite(user_id=user_id, listing_id=listing_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def remove_favorite(db: Session, user_id: int, listing_id: int) -> bool:
    """Remove a listing from favorites."""
    favorite = (db.query(Favorite)
                .filter(and_(Favorite.user_id == user_id, 
                           Favorite.listing_id == listing_id))
                .first())
    
    if not favorite:
        return False
    
    db.delete(favorite)
    db.commit()
    return True


# Review CRUD operations
def get_user_reviews(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Review]:
    """Get reviews for a user."""
    return (db.query(Review)
            .filter(Review.reviewed_user_id == user_id)
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
            .all())


def create_review(
    db: Session,
    reviewer_id: int,
    reviewed_user_id: int,
    rating: int,
    comment: Optional[str] = None,
    listing_id: Optional[int] = None
) -> Review:
    """Create a new review."""
    db_review = Review(
        reviewer_id=reviewer_id,
        reviewed_user_id=reviewed_user_id,
        rating=rating,
        comment=comment,
        listing_id=listing_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_user_average_rating(db: Session, user_id: int) -> float:
    """Get average rating for a user."""
    from sqlalchemy import func
    
    result = (db.query(func.avg(Review.rating))
              .filter(Review.reviewed_user_id == user_id)
              .scalar())
    
    return float(result) if result else 0.0


# SavedSearch CRUD operations
def get_user_saved_searches(
    db: Session, 
    user_id: int
) -> List[SavedSearch]:
    """Get all saved searches for a user."""
    return (db.query(SavedSearch)
            .filter(SavedSearch.user_id == user_id)
            .order_by(desc(SavedSearch.created_at))
            .all())


def create_saved_search(
    db: Session,
    user_id: int,
    name: str,
    search_query: Optional[str] = None,
    category: Optional[str] = None,
    location: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    filters: Optional[str] = None
) -> SavedSearch:
    """Create a new saved search."""
    db_search = SavedSearch(
        user_id=user_id,
        name=name,
        search_query=search_query,
        category=category,
        location=location,
        min_price=min_price,
        max_price=max_price,
        filters=filters
    )
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    return db_search


def delete_saved_search(db: Session, search_id: int) -> bool:
    """Delete a saved search."""
    search = db.query(SavedSearch).filter(SavedSearch.id == search_id).first()
    if not search:
        return False
    
    db.delete(search)
    db.commit()
    return True
