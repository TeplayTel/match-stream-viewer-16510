from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router

app = FastAPI(
    title="OTT Match Streaming Backend API",
    description="Backend API for OTT application providing match details, team info, and emoji reaction tracking.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Match", "description": "Match details and streaming info"},
        {"name": "Teams", "description": "Teams and players info"},
        {"name": "Emoji", "description": "Emoji reactions"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API endpoints under "/api"
app.include_router(router, prefix="/api")

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to make sure app is running."""
    return {"message": "Healthy"}
