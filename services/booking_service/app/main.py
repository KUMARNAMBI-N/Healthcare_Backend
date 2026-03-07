import sys
from pathlib import Path

# Add project root to python path to resolve 'services' module
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI
from services.booking_service.app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME + " - Booking Service",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Booking Service"}
