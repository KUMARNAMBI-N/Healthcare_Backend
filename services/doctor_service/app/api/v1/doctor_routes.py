from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

from services.doctor_service.app.db.session import get_db_session
from services.doctor_service.app.schemas.doctor_schema import DoctorCreate, DoctorResponse, DoctorUpdate, DoctorProfileResponse
from services.doctor_service.app.schemas.education_schema import EducationCreate, EducationResponse
from services.doctor_service.app.schemas.experience_schema import ExperienceCreate, ExperienceResponse
from services.doctor_service.app.schemas.language_schema import LanguageCreate, LanguageResponse
from services.doctor_service.app.services.doctor_service import DoctorService

# TODO: Add actual security dependencies (e.g., JWT extraction)
def get_current_user_placeholder():
    return {"user_id": "placeholder", "role": "admin"}

router = APIRouter()

def get_doctor_service(db: AsyncSession = Depends(get_db_session)) -> DoctorService:
    return DoctorService(db)

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    doctor_in: DoctorCreate, 
    service: DoctorService = Depends(get_doctor_service),
    current_user: dict = Depends(get_current_user_placeholder)
):
    """
    Create a new doctor profile.
    Time Complexity: O(1)
    """
    return await service.create_doctor(doctor_in)

@router.get("/", response_model=List[DoctorResponse])
async def list_doctors(
    specialization_id: Optional[str] = None,
    hospital_id: Optional[str] = None,
    min_experience: Optional[int] = None,
    rating: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    service: DoctorService = Depends(get_doctor_service)
):
    """
    List doctors with filtering and pagination.
    Time Complexity: O(log n) with indexes
    """
    skip = (page - 1) * limit
    filters = {
        "specialization_id": specialization_id,
        "hospital_id": hospital_id,
        "min_experience": min_experience,
        "rating": rating,
        "skip": skip,
        "limit": limit
    }
    return await service.list_doctors(filters)

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: str, service: DoctorService = Depends(get_doctor_service)):
    """
    Get a specific doctor profile by ID.
    Time Complexity: O(1)
    """
    return await service.get_doctor(doctor_id)

@router.get("/{doctor_id}/profile", response_model=DoctorProfileResponse)
async def get_doctor_profile(doctor_id: str, service: DoctorService = Depends(get_doctor_service)):
    """
    Get a specific doctor's full aggregated profile (including nested education, etc.).
    Time Complexity: O(k) where k is related rows
    """
    return await service.get_doctor_profile(doctor_id)

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(
    doctor_id: str, 
    doctor_update: DoctorUpdate, 
    service: DoctorService = Depends(get_doctor_service),
    current_user: dict = Depends(get_current_user_placeholder)
):
    """
    Update a doctor profile.
    """
    return await service.update_doctor(doctor_id, doctor_update)

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor_id: str, 
    service: DoctorService = Depends(get_doctor_service),
    current_user: dict = Depends(get_current_user_placeholder)
):
    """
    Delete a doctor profile.
    """
    await service.delete_doctor(doctor_id)
    return None

# Sub-resources
@router.post("/{doctor_id}/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    doctor_id: str, 
    edu_in: EducationCreate, 
    service: DoctorService = Depends(get_doctor_service)
):
    return await service.add_education(doctor_id, edu_in)

@router.post("/{doctor_id}/experience", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def add_experience(
    doctor_id: str, 
    exp_in: ExperienceCreate, 
    service: DoctorService = Depends(get_doctor_service)
):
    return await service.add_experience(doctor_id, exp_in)

@router.post("/{doctor_id}/languages", response_model=LanguageResponse, status_code=status.HTTP_201_CREATED)
async def add_language(
    doctor_id: str, 
    lang_in: LanguageCreate, 
    service: DoctorService = Depends(get_doctor_service)
):
    return await service.add_language(doctor_id, lang_in)
