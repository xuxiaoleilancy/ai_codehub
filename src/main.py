from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from src.api.routers import model_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI CodeHub - A platform for managing and sharing AI models",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(model_router.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI CodeHub",
        "version": "1.0.0",
        "status": "running",
        "docs_url": "/docs",
        "api_version": settings.API_V1_STR
    }

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 