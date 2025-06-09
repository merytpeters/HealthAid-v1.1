from backend.app.core.config import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=True
    )
