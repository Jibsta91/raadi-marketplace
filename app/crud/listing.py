from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from app.models.listing import Listing, ListingStatus, ListingType
from app.schemas.listing import ListingCreate, ListingUpdate


def get_listing(db: Session, listing_id: int) -> Optional[Listing]:
    """Get a listing by ID."""
    return db.query(Listing).filter(Listing.id == listing_id).first()


def get_listing_by_id(db: Session, listing_id: int) -> Optional[Listing]:
    """Get a listing by ID (alias for get_listing)."""
    return get_listing(db, listing_id)


def get_listings(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category: Optional[str] = None,
    location: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    listing_type: Optional[str] = None,
    status: Optional[str] = None,
    seller_id: Optional[int] = None
) -> List[Listing]:
    """Get listings with optional filtering."""
    query = db.query(Listing)
    
    # Apply filters
    if category:
        query = query.filter(Listing.category == category)
    if location:
        query = query.filter(Listing.location.ilike(f"%{location}%"))
    if min_price:
        query = query.filter(Listing.price >= min_price)
    if max_price:
        query = query.filter(Listing.price <= max_price)
    if listing_type:
        query = query.filter(Listing.listing_type == listing_type)
    if status:
        query = query.filter(Listing.status == status)
    if seller_id:
        query = query.filter(Listing.seller_id == seller_id)
    
    # Only show approved listings
    query = query.filter(Listing.is_approved == True)
    
    return query.order_by(desc(Listing.created_at)).offset(skip).limit(limit).all()


def search_listings(
    db: Session,
    search_query: str,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None
) -> List[Listing]:
    """Search listings by title and description."""
    query = db.query(Listing)
    
    # Text search in title and description
    search_filter = or_(
        Listing.title.ilike(f"%{search_query}%"),
        Listing.description.ilike(f"%{search_query}%")
    )
    query = query.filter(search_filter)
    
    # Category filter
    if category:
        query = query.filter(Listing.category == category)
    
    # Only show approved listings
    query = query.filter(Listing.is_approved == True)
    
    return query.order_by(desc(Listing.created_at)).offset(skip).limit(limit).all()


def get_featured_listings(db: Session, limit: int = 10) -> List[Listing]:
    """Get featured listings."""
    return (db.query(Listing)
            .filter(and_(Listing.is_featured == True, 
                        Listing.is_approved == True,
                        Listing.status == ListingStatus.ACTIVE))
            .order_by(desc(Listing.created_at))
            .limit(limit)
            .all())


def get_promoted_listings(db: Session, limit: int = 10) -> List[Listing]:
    """Get promoted listings."""
    return (db.query(Listing)
            .filter(and_(Listing.is_promoted == True, 
                        Listing.is_approved == True,
                        Listing.status == ListingStatus.ACTIVE))
            .order_by(desc(Listing.last_bumped))
            .limit(limit)
            .all())


def get_user_listings(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Listing]:
    """Get all listings by a specific user."""
    return (db.query(Listing)
            .filter(Listing.seller_id == user_id)
            .order_by(desc(Listing.created_at))
            .offset(skip)
            .limit(limit)
            .all())


def create_listing(db: Session, listing: ListingCreate, seller_id: int) -> Listing:
    """Create a new listing."""
    db_listing = Listing(
        **listing.dict(exclude_unset=True),
        seller_id=seller_id
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


def update_listing(
    db: Session, 
    listing_id: int, 
    listing_update: ListingUpdate
) -> Optional[Listing]:
    """Update a listing."""
    db_listing = get_listing(db, listing_id)
    if not db_listing:
        return None
    
    update_data = listing_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_listing, field, value)
    
    db.commit()
    db.refresh(db_listing)
    return db_listing


def delete_listing(db: Session, listing_id: int) -> bool:
    """Delete a listing."""
    db_listing = get_listing(db, listing_id)
    if not db_listing:
        return False
    
    db.delete(db_listing)
    db.commit()
    return True


def increment_view_count(db: Session, listing_id: int) -> Optional[Listing]:
    """Increment view count for a listing."""
    db_listing = get_listing(db, listing_id)
    if db_listing:
        db_listing.view_count += 1
        db.commit()
        db.refresh(db_listing)
    return db_listing


def bump_listing(db: Session, listing_id: int) -> Optional[Listing]:
    """Bump a listing (update last_bumped timestamp)."""
    from datetime import datetime
    
    db_listing = get_listing(db, listing_id)
    if db_listing:
        db_listing.bump_count += 1
        db_listing.last_bumped = datetime.utcnow()
        db.commit()
        db.refresh(db_listing)
    return db_listing


def mark_as_sold(db: Session, listing_id: int) -> Optional[Listing]:
    """Mark a listing as sold."""
    from datetime import datetime
    
    db_listing = get_listing(db, listing_id)
    if db_listing:
        db_listing.status = ListingStatus.SOLD
        db_listing.sold_at = datetime.utcnow()
        db.commit()
        db.refresh(db_listing)
    return db_listing


def get_listings_by_category(
    db: Session, 
    category: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[Listing]:
    """Get listings by category."""
    return (db.query(Listing)
            .filter(and_(Listing.category == category, 
                        Listing.is_approved == True,
                        Listing.status == ListingStatus.ACTIVE))
            .order_by(desc(Listing.created_at))
            .offset(skip)
            .limit(limit)
            .all())
