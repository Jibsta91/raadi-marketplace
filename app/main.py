from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.core.monitoring import (
    setup_sentry, 
    setup_logging, 
    MetricsMiddleware,
    get_metrics
)
from app.core.cache import cache
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    setup_logging()
    setup_sentry()
    await cache.connect()
    yield
    # Shutdown
    await cache.disconnect()


app = FastAPI(
    title="Raadi Enterprise Marketplace",
    description="Norwegian enterprise marketplace webapp",
    version=settings.VERSION,
    lifespan=lifespan
)

# Add security and monitoring middleware
if settings.ENABLE_METRICS:
    app.add_middleware(MetricsMiddleware)

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": int(time.time())
    }


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    if settings.ENABLE_METRICS:
        return Response(content=get_metrics(), media_type="text/plain")
    return {"error": "Metrics disabled"}


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
