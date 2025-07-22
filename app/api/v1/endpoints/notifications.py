from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_notifications():
    """Get user notifications"""
    return {"notifications": []}


@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: int):
    """Mark notification as read"""
    return {"message": "Marked as read"}
