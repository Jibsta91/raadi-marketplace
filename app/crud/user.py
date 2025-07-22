from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    db_user = User(
        email=user.email,
        hashed_password=user.password,  # Already hashed in auth endpoint
        full_name=user.full_name,
        phone=user.phone,
        location=user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def update_user(db: Session, user_id: int, user_update: dict) -> Optional[User]:
    """Update user information"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    for field, value in user_update.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_stats(db: Session, user_id: int, **stats) -> Optional[User]:
    """Update user statistics"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    if 'total_listings' in stats:
        db_user.total_listings = stats['total_listings']
    if 'total_reviews' in stats:
        db_user.total_reviews = stats['total_reviews']
    if 'average_rating' in stats:
        db_user.average_rating = stats['average_rating']
    
    db.commit()
    db.refresh(db_user)
    return db_user
