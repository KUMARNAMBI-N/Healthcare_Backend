import sys
from pathlib import Path

# Add project root to python path to resolve 'services' module
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.hospital_service.app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservice managing hospital data and facilities",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Hospital Service", "status": "active"}

from services.hospital_service.app.api.v1 import hospital_routes
app.include_router(hospital_routes.router, prefix=f"{settings.API_V1_STR}/hospitals", tags=["Hospitals"])
