from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from services.doctor_service.app.schemas.education_schema import EducationResponse
from services.doctor_service.app.schemas.experience_schema import ExperienceResponse
from services.doctor_service.app.schemas.language_schema import LanguageResponse

class DoctorBase(BaseModel):
    hospital_id: Optional[str] = None
    organization_id: Optional[str] = None
    full_name: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr
    specialization_id: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: int = Field(default=0, ge=0)
    consultation_fee: float = Field(default=0.0, ge=0.0)
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool = True

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    hospital_id: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialization_id: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0)
    consultation_fee: Optional[float] = Field(None, ge=0.0)
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: Optional[bool] = None

class DoctorResponse(DoctorBase):
    id: str
    rating: float
    total_reviews: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DoctorProfileResponse(DoctorResponse):
    educations: List[EducationResponse] = []
    experiences: List[ExperienceResponse] = []
    languages: List[LanguageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
