from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1 import analysis, auth, profiles, platforms
from app.api.v1 import ai_analysis
from app.core.config import settings
from app.db.database import engine, Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create uploads directory if it doesn't exist
os.makedirs("uploads/resumes", exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="ElevateAI API",
    description="AI-Powered Career Enhancement Tool - Backend API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    profiles.router,
    prefix="/api/v1/profiles",
    tags=["Profiles"]
)

app.include_router(
    platforms.router,
    prefix="/api/v1/platforms",
    tags=["Platforms"]
)

app.include_router(
    analysis.router,
    prefix="/api/v1/analyze",
    tags=["Analysis"]
)

app.include_router(
    ai_analysis.router,
    prefix="/api/v1/ai",
    tags=["AI Analysis"]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ElevateAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "debug": settings.DEBUG
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
