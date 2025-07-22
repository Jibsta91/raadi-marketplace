from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Raadi Enterprise Marketplace",
    description="Norwegian enterprise marketplace webapp",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve HTML pages
@app.get("/")
async def serve_index():
    """Serve the main index page"""
    return FileResponse("static/index.html")


@app.get("/browse")
async def serve_browse():
    """Serve the browse page"""
    return FileResponse("static/browse.html")


@app.get("/login")
async def serve_login():
    """Serve the login page"""
    return FileResponse("static/login.html")


@app.get("/register")
async def serve_register():
    """Serve the register page"""
    return FileResponse("static/register.html")


@app.get("/governance-dashboard")
async def serve_governance_dashboard():
    """Serve the AI governance dashboard"""
    return FileResponse("static/governance-dashboard.html")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "raadi-marketplace"}


# Temporary API endpoints for testing
@app.get("/api/test")
async def test_api():
    """Test API endpoint"""
    return {"message": "API is working!", "status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
