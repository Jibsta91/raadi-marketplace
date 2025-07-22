from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_categories():
    """Get all marketplace categories"""
    categories = {
        "torget": {
            "name": "Torget",
            "description": "General marketplace/classified ads",
            "icon": "shopping-bag",
            "subcategories": [
                {"id": "furniture", "name": "Møbler", "count": 1234},
                {"id": "electronics", "name": "Elektronikk", "count": 892},
                {"id": "clothing", "name": "Klær", "count": 2156},
                {"id": "books", "name": "Bøker", "count": 567},
                {"id": "sports", "name": "Sport", "count": 789}
            ]
        },
        "jobb": {
            "name": "Jobb",
            "description": "Job listings and career opportunities", 
            "icon": "briefcase",
            "subcategories": [
                {"id": "full_time", "name": "Heltid", "count": 456},
                {"id": "part_time", "name": "Deltid", "count": 234},
                {"id": "freelance", "name": "Freelance", "count": 123},
                {"id": "internship", "name": "Praktikant", "count": 67}
            ]
        },
        "bil_og_campingvogn": {
            "name": "Bil og campingvogn",
            "description": "Cars and camping vehicles",
            "icon": "car",
            "subcategories": [
                {"id": "cars", "name": "Biler", "count": 3456},
                {"id": "camping", "name": "Campingvogner", "count": 234},
                {"id": "parts", "name": "Bildeler", "count": 567}
            ]
        },
        "eiendom": {
            "name": "Eiendom",
            "description": "Real estate",
            "icon": "home",
            "subcategories": [
                {"id": "for_sale", "name": "Til salgs", "count": 1234},
                {"id": "for_rent", "name": "Til leie", "count": 890},
                {"id": "commercial", "name": "Næringseiendom", "count": 123},
                {"id": "land", "name": "Tomter", "count": 234}
            ]
        },
        "reise": {
            "name": "Reise",
            "description": "Travel services",
            "icon": "plane",
            "subcategories": [
                {"id": "vacation_rentals", "name": "Ferieutleie", "count": 456},
                {"id": "package_deals", "name": "Pakkereiser", "count": 123},
                {"id": "flights", "name": "Flyreiser", "count": 89},
                {"id": "hotels", "name": "Hotell", "count": 234}
            ]
        },
        "bat": {
            "name": "Båt",
            "description": "Boats and marine vehicles",
            "icon": "anchor",
            "subcategories": [
                {"id": "motor_boats", "name": "Motorbåter", "count": 234},
                {"id": "sail_boats", "name": "Seilbåter", "count": 123},
                {"id": "jet_ski", "name": "Vannscooter", "count": 56},
                {"id": "marine_equipment", "name": "Marin utstyr", "count": 189}
            ]
        },
        "mc": {
            "name": "MC",
            "description": "Motorcycles",
            "icon": "motorcycle",
            "subcategories": [
                {"id": "sport_bikes", "name": "Sportsbike", "count": 123},
                {"id": "cruisers", "name": "Cruiser", "count": 89},
                {"id": "touring", "name": "Touring", "count": 45},
                {"id": "accessories", "name": "Tilbehør", "count": 234}
            ]
        },
        "nyttekjoretoy": {
            "name": "Nyttekjøretøy og maskiner",
            "description": "Commercial vehicles and machinery",
            "icon": "truck",
            "subcategories": [
                {"id": "trucks", "name": "Lastebiler", "count": 234},
                {"id": "vans", "name": "Varebiler", "count": 345},
                {"id": "construction", "name": "Anleggsmaskiner", "count": 123},
                {"id": "agricultural", "name": "Landbruksmaskiner", "count": 89}
            ]
        }
    }
    
    return categories


@router.get("/{category_id}")
async def get_category(category_id: str):
    """Get specific category details"""
    # This would normally fetch from database
    return {
        "id": category_id,
        "name": "Category Name",
        "description": "Category description",
        "listing_count": 1234,
        "featured_listings": []
    }
