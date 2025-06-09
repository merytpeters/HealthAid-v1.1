import os
import uvicorn
from backend.app.core.config import settings

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.PORT))  # fallback to settings.PORT if PORT is not set
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
