from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.listing import (
    ListingCreate, ListingUpdate, ListingResponse, ListingSearch
)
from app.crud import listing as crud_listing
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ListingResponse])
def get_listings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    category: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    listing_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get listings with optional filtering."""
    listings = crud_listing.get_listings(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        location=location,
        min_price=min_price,
        max_price=max_price,
        listing_type=listing_type,
        status=status
    )
    return listings


@router.get("/search", response_model=List[ListingResponse])
def search_listings(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Search listings by title and description."""
    listings = crud_listing.search_listings(
        db=db,
        search_query=q,
        skip=skip,
        limit=limit,
        category=category
    )
    return listings


@router.get("/featured", response_model=List[ListingResponse])
def get_featured_listings(
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """Get featured listings."""
    return crud_listing.get_featured_listings(db=db, limit=limit)


@router.get("/promoted", response_model=List[ListingResponse])
def get_promoted_listings(
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """Get promoted listings."""
    return crud_listing.get_promoted_listings(db=db, limit=limit)


@router.get("/category/{category}", response_model=List[ListingResponse])
def get_listings_by_category(
    category: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get listings by category."""
    listings = crud_listing.get_listings_by_category(
        db=db,
        category=category,
        skip=skip,
        limit=limit
    )
    return listings


@router.get("/{listing_id}", response_model=ListingResponse)
def get_listing(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific listing by ID."""
    listing = crud_listing.get_listing(db=db, listing_id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Increment view count
    crud_listing.increment_view_count(db=db, listing_id=listing_id)
    
    return listing


@router.post("/", response_model=ListingResponse)
def create_listing(
    listing: ListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new listing."""
    return crud_listing.create_listing(
        db=db, 
        listing=listing, 
        seller_id=current_user.id
    )


@router.put("/{listing_id}", response_model=ListingResponse)
def update_listing(
    listing_id: int,
    listing_update: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a listing."""
    # Check if listing exists
    existing_listing = crud_listing.get_listing(db=db, listing_id=listing_id)
    if not existing_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check if user owns the listing
    if existing_listing.seller_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to update this listing"
        )
    
    updated_listing = crud_listing.update_listing(
        db=db, 
        listing_id=listing_id, 
        listing_update=listing_update
    )
    return updated_listing


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a listing."""
    # Check if listing exists
    existing_listing = crud_listing.get_listing(db=db, listing_id=listing_id)
    if not existing_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check if user owns the listing
    if existing_listing.seller_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to delete this listing"
        )
    
    success = crud_listing.delete_listing(db=db, listing_id=listing_id)
    if not success:
        raise HTTPException(
            status_code=500, 
            detail="Failed to delete listing"
        )
    
    return {"message": "Listing deleted successfully"}


@router.post("/{listing_id}/bump")
def bump_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bump a listing to increase visibility."""
    # Check if listing exists
    existing_listing = crud_listing.get_listing(db=db, listing_id=listing_id)
    if not existing_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check if user owns the listing
    if existing_listing.seller_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to bump this listing"
        )
    
    bumped_listing = crud_listing.bump_listing(db=db, listing_id=listing_id)
    return {"message": "Listing bumped successfully", "listing": bumped_listing}


@router.post("/{listing_id}/mark-sold")
def mark_listing_as_sold(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a listing as sold."""
    # Check if listing exists
    existing_listing = crud_listing.get_listing(db=db, listing_id=listing_id)
    if not existing_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check if user owns the listing
    if existing_listing.seller_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to modify this listing"
        )
    
    sold_listing = crud_listing.mark_as_sold(db=db, listing_id=listing_id)
    return {"message": "Listing marked as sold", "listing": sold_listing}


@router.get("/user/{user_id}", response_model=List[ListingResponse])
def get_user_listings(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get all listings by a specific user."""
    listings = crud_listing.get_user_listings(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit
    )
    return listings
