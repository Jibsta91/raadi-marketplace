from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def search_listings(
    q: str = "",
    category: str = None,
    location: str = None,
    price_min: int = None,
    price_max: int = None,
    page: int = 1,
    limit: int = 20
):
    """Search marketplace listings"""
    # Mock search results
    results = {
        "query": q,
        "total_results": 1247,
        "page": page,
        "limit": limit,
        "total_pages": 63,
        "results": [
            {
                "id": 12345,
                "title": "Tesla Model 3 - 2023",
                "description": "Excellent condition Tesla Model 3...",
                "price": 450000,
                "currency": "NOK",
                "category": "bil_og_campingvogn",
                "location": "Oslo",
                "images": ["image1.jpg", "image2.jpg"],
                "created_at": "2025-01-20T10:00:00Z",
                "featured": True
            },
            {
                "id": 12346,
                "title": "Modern Sofa - Like New",
                "description": "Beautiful modern sofa in excellent condition...",
                "price": 8500,
                "currency": "NOK", 
                "category": "torget",
                "location": "Bergen",
                "images": ["sofa1.jpg"],
                "created_at": "2025-01-21T14:30:00Z",
                "featured": False
            }
        ],
        "facets": {
            "categories": {
                "bil_og_campingvogn": 456,
                "torget": 321,
                "eiendom": 234,
                "jobb": 123
            },
            "locations": {
                "Oslo": 345,
                "Bergen": 234,
                "Trondheim": 123,
                "Stavanger": 89
            },
            "price_ranges": {
                "0-1000": 123,
                "1000-10000": 234,
                "10000-100000": 345,
                "100000+": 234
            }
        }
    }
    
    return results


@router.get("/suggestions")
async def get_search_suggestions(q: str):
    """Get search suggestions"""
    suggestions = [
        "tesla model 3",
        "tesla model s", 
        "tesla model x",
        "electric car",
        "used car oslo"
    ]
    
    return {"suggestions": suggestions[:5]}


@router.get("/trending")
async def get_trending_searches():
    """Get trending search terms"""
    trending = [
        "electric cars",
        "apartments oslo",
        "iphone 15",
        "winter clothes",
        "ski equipment"
    ]
    
    return {"trending": trending}
