import sys
from pathlib import Path

# Add project root to python path to resolve 'services' module
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.doctor_service.app.core.config import settings
from services.doctor_service.app.api.v1 import doctor_routes
from services.doctor_service.app.api.v1 import specialization_routes

app = FastAPI(
    title=settings.PROJECT_NAME + " - Doctor Service",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Doctor Service"}

app.include_router(doctor_routes.router, prefix=f"{settings.API_V1_STR}/doctors", tags=["Doctors"])
app.include_router(specialization_routes.router, prefix=f"{settings.API_V1_STR}/specializations", tags=["Specializations"])
