from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.message import (
    MessageCreate, MessageResponse, FavoriteResponse, ReviewCreate, 
    ReviewResponse, SavedSearchCreate, SavedSearchResponse
)
from app.crud import message as crud_message
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


# Message endpoints
@router.get("/", response_model=List[MessageResponse])
def get_user_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all messages for the current user."""
    messages = crud_message.get_user_messages(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return messages


@router.get("/conversation/{other_user_id}", response_model=List[MessageResponse])
def get_conversation(
    other_user_id: int,
    listing_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get conversation between current user and another user."""
    messages = crud_message.get_conversation(
        db=db,
        user1_id=current_user.id,
        user2_id=other_user_id,
        listing_id=listing_id
    )
    return messages


@router.post("/", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a new message."""
    db_message = crud_message.create_message(
        db=db,
        sender_id=current_user.id,
        recipient_id=message.recipient_id,
        content=message.content,
        subject=message.subject,
        listing_id=message.listing_id,
        thread_id=message.thread_id
    )
    return db_message


@router.put("/{message_id}/read")
def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a message as read."""
    # Check if message exists and user is recipient
    message = crud_message.get_message(db=db, message_id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.recipient_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to mark this message as read"
        )
    
    updated_message = crud_message.mark_message_as_read(
        db=db, 
        message_id=message_id
    )
    return {"message": "Message marked as read", "data": updated_message}


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a message."""
    # Check if message exists and user owns it
    message = crud_message.get_message(db=db, message_id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to delete this message"
        )
    
    success = crud_message.delete_message(db=db, message_id=message_id)
    if not success:
        raise HTTPException(
            status_code=500, 
            detail="Failed to delete message"
        )
    
    return {"message": "Message deleted successfully"}


# Favorite endpoints
@router.get("/favorites", response_model=List[FavoriteResponse])
def get_user_favorites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all favorites for the current user."""
    favorites = crud_message.get_user_favorites(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return favorites


@router.post("/favorites/{listing_id}")
def add_favorite(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a listing to favorites."""
    favorite = crud_message.add_favorite(
        db=db,
        user_id=current_user.id,
        listing_id=listing_id
    )
    
    if not favorite:
        raise HTTPException(
            status_code=400, 
            detail="Listing is already in favorites"
        )
    
    return {"message": "Listing added to favorites", "favorite": favorite}


@router.delete("/favorites/{listing_id}")
def remove_favorite(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a listing from favorites."""
    success = crud_message.remove_favorite(
        db=db,
        user_id=current_user.id,
        listing_id=listing_id
    )
    
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Favorite not found"
        )
    
    return {"message": "Listing removed from favorites"}


@router.get("/favorites/{listing_id}/check")
def check_favorite(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if a listing is favorited by the current user."""
    is_fav = crud_message.is_favorite(
        db=db,
        user_id=current_user.id,
        listing_id=listing_id
    )
    return {"is_favorite": is_fav}


# Review endpoints
@router.get("/reviews/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get reviews for a specific user."""
    reviews = crud_message.get_user_reviews(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    return reviews


@router.post("/reviews", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new review."""
    db_review = crud_message.create_review(
        db=db,
        reviewer_id=current_user.id,
        reviewed_user_id=review.reviewed_user_id,
        rating=review.rating,
        comment=review.comment,
        listing_id=review.listing_id
    )
    return db_review


@router.get("/reviews/{user_id}/average")
def get_user_average_rating(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get average rating for a user."""
    avg_rating = crud_message.get_user_average_rating(db=db, user_id=user_id)
    return {"user_id": user_id, "average_rating": avg_rating}


# Saved search endpoints
@router.get("/saved-searches", response_model=List[SavedSearchResponse])
def get_user_saved_searches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all saved searches for the current user."""
    searches = crud_message.get_user_saved_searches(
        db=db,
        user_id=current_user.id
    )
    return searches


@router.post("/saved-searches", response_model=SavedSearchResponse)
def create_saved_search(
    search: SavedSearchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new saved search."""
    db_search = crud_message.create_saved_search(
        db=db,
        user_id=current_user.id,
        **search.dict()
    )
    return db_search


@router.delete("/saved-searches/{search_id}")
def delete_saved_search(
    search_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a saved search."""
    success = crud_message.delete_saved_search(db=db, search_id=search_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Saved search not found"
        )
    
    return {"message": "Saved search deleted successfully"}
