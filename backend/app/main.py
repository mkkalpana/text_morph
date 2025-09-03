# FastAPI Main Application
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.config import settings
from app.database import init_db
from app.routers import auth, users, analysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AI Text Summarization API",
    description="Professional Backend API for Text Analysis and User Management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "status_code": 500
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        logger.info("Starting AI Text Summarization API...")
        init_db()
        logger.info("Database initialized successfully")
        logger.info("API is ready to accept requests")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

# Root endpoint
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "AI Text Summarization API",
        "version": "2.0.0",
        "status": "active",
        "features": [
            "User Authentication & Management",
            "File Upload & Text Analysis",
            "Readability Scoring",
            "Professional Dashboard"
        ],
        "endpoints": {
            "docs": "/docs",
            "auth": "/api/auth",
            "users": "/api/users",
            "analysis": "/api/analysis"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "success": True,
        "status": "healthy",
        "message": "API is running",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)