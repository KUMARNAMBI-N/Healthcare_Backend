from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from services.hospital_service.app.db.session import get_db_session
from services.hospital_service.app.services.hospital_service import HospitalService
from services.hospital_service.app.schemas.hospital_schema import (
    HospitalCreate, HospitalUpdate, 
    PaginatedHospitalResponse, SingleHospitalResponse
)

router = APIRouter()

def get_hospital_service(session: AsyncSession = Depends(get_db_session)) -> HospitalService:
    return HospitalService(session)

@router.post("/", response_model=SingleHospitalResponse, status_code=201)
async def create_hospital(
    hospital_in: HospitalCreate,
    service: HospitalService = Depends(get_hospital_service)
):
    """Create a new hospital with optional facilities and images."""
    return await service.create_hospital(hospital_in)

@router.get("/nearby")
async def get_nearby_hospitals(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude of the center point"),
    lng: float = Query(..., ge=-180.0, le=180.0, description="Longitude of the center point"),
    radius_km: float = Query(10.0, gt=0, description="Search radius in kilometers"),
    service: HospitalService = Depends(get_hospital_service)
):
    """Find hospitals within a given radius using geospatial distance."""
    return await service.find_nearby(lat=lat, lng=lng, radius_km=radius_km)

@router.get("/{hospital_id}", response_model=SingleHospitalResponse)
async def get_hospital(
    hospital_id: str = Path(...),
    service: HospitalService = Depends(get_hospital_service)
):
    """Retrieve a hospital by its ID."""
    return await service.get_hospital(hospital_id)

@router.put("/{hospital_id}", response_model=SingleHospitalResponse)
async def update_hospital(
    hospital_in: HospitalUpdate,
    hospital_id: str = Path(...),
    service: HospitalService = Depends(get_hospital_service)
):
    """Update details of a hospital."""
    return await service.update_hospital(hospital_id, hospital_in)

@router.delete("/{hospital_id}")
async def delete_hospital(
    hospital_id: str = Path(...),
    service: HospitalService = Depends(get_hospital_service)
):
    """Delete a hospital."""
    return await service.delete_hospital(hospital_id)

@router.get("/", response_model=PaginatedHospitalResponse)
async def list_hospitals(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    city: Optional[str] = Query(None, description="Filter by city name"),
    rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Filter by minimum rating"),
    organization_id: Optional[str] = Query(None, description="Filter by organization UUID"),
    service: HospitalService = Depends(get_hospital_service)
):
    """List hospitals with optional filtering and pagination."""
    return await service.list_hospitals(
        page=page, limit=limit, city=city, rating=rating, organization_id=organization_id
    )
