"""Main FastAPI Entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router

app = FastAPI()
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for development; restrict in production
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)


@app.get("/")
async def root():
    """Root check"""
    return {"message": "Welcome to the Healthaid API!"}


@app.get("/health")
async def health_check():
    """Health Check"""
    return {"status": "ok"}


@app.get("/version")
async def version():
    """Version Check"""
    return {
        "version": "1.0.0",
        "description": "Healthaid application with user authentication",
    }
