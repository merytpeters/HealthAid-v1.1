# Main FastAPI entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes.auth import router as auth_router

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
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Healthaid API!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/version")
async def version():
    return {
        "version": "1.0.0", "description":
            "Healthaid application with user authentication"
    }
