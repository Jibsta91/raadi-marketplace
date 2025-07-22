from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, categories, search, business, 
    notifications, listings, messages,
    ai_governance, ai_cybersecurity, ai_infrastructure, ai_datamanagement
)

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# User routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Listing routes
api_router.include_router(listings.router, prefix="/listings", tags=["listings"])

# Message routes (includes messages, favorites, reviews, saved searches)
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])

# Category routes
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])

# Search routes
api_router.include_router(search.router, prefix="/search", tags=["search"])

# Business routes
api_router.include_router(business.router, prefix="/business", tags=["business"])

# Notification routes
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

# AI services routes
api_router.include_router(ai_governance.router, prefix="/ai/governance", tags=["ai-governance"])
api_router.include_router(ai_cybersecurity.router, prefix="/ai/cybersecurity", tags=["ai-cybersecurity"])
api_router.include_router(ai_infrastructure.router, prefix="/ai/infrastructure", tags=["ai-infrastructure"])
api_router.include_router(ai_datamanagement.router, prefix="/ai/datamanagement", tags=["ai-datamanagement"])