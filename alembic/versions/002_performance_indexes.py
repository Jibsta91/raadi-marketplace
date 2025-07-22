"""Add performance indexes

Revision ID: 002_performance_indexes
Revises: 001_initial
Create Date: 2025-01-21 12:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002_performance_indexes'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    """Add indexes for improved query performance"""
    
    # Listings table indexes
    op.create_index('idx_listings_category', 'listings', ['category'])
    op.create_index('idx_listings_location', 'listings', ['location'])
    op.create_index('idx_listings_created_at', 'listings', ['created_at'])
    op.create_index('idx_listings_is_active', 'listings', ['is_active'])
    op.create_index('idx_listings_price', 'listings', ['price'])
    op.create_index('idx_listings_user_id', 'listings', ['user_id'])
    
    # Composite indexes for common query patterns
    op.create_index('idx_listings_category_location', 'listings', ['category', 'location'])
    op.create_index('idx_listings_category_active', 'listings', ['category', 'is_active'])
    op.create_index('idx_listings_location_active', 'listings', ['location', 'is_active'])
    
    # Users table indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_is_active', 'users', ['is_active'])
    op.create_index('idx_users_created_at', 'users', ['created_at'])
    
    # Messages table indexes
    op.create_index('idx_messages_sender_id', 'messages', ['sender_id'])
    op.create_index('idx_messages_recipient_id', 'messages', ['recipient_id'])
    op.create_index('idx_messages_listing_id', 'messages', ['listing_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])
    op.create_index('idx_messages_is_read', 'messages', ['is_read'])
    
    # Favorites table indexes
    op.create_index('idx_favorites_user_id', 'favorites', ['user_id'])
    op.create_index('idx_favorites_listing_id', 'favorites', ['listing_id'])
    op.create_index('idx_favorites_created_at', 'favorites', ['created_at'])
    
    # Reviews table indexes
    op.create_index('idx_reviews_reviewer_id', 'reviews', ['reviewer_id'])
    op.create_index('idx_reviews_reviewed_user_id', 'reviews', ['reviewed_user_id'])
    op.create_index('idx_reviews_listing_id', 'reviews', ['listing_id'])
    op.create_index('idx_reviews_rating', 'reviews', ['rating'])
    op.create_index('idx_reviews_created_at', 'reviews', ['created_at'])


def downgrade():
    """Remove performance indexes"""
    
    # Drop all indexes created in upgrade
    indexes_to_drop = [
        'idx_listings_category',
        'idx_listings_location', 
        'idx_listings_created_at',
        'idx_listings_is_active',
        'idx_listings_price',
        'idx_listings_user_id',
        'idx_listings_category_location',
        'idx_listings_category_active',
        'idx_listings_location_active',
        'idx_users_email',
        'idx_users_is_active',
        'idx_users_created_at',
        'idx_messages_sender_id',
        'idx_messages_recipient_id',
        'idx_messages_listing_id',
        'idx_messages_created_at',
        'idx_messages_is_read',
        'idx_favorites_user_id',
        'idx_favorites_listing_id',
        'idx_favorites_created_at',
        'idx_reviews_reviewer_id',
        'idx_reviews_reviewed_user_id',
        'idx_reviews_listing_id',
        'idx_reviews_rating',
        'idx_reviews_created_at',
    ]
    
    for index_name in indexes_to_drop:
        op.drop_index(index_name)
