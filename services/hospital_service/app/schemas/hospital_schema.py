from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

# --- Hospital Facility Schemas --- #
class FacilityBase(BaseModel):
    facility_name: str = Field(..., min_length=2, max_length=255, examples=["ICU"])

class FacilityCreate(FacilityBase):
    pass

class FacilityResponse(FacilityBase):
    id: str
    hospital_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Hospital Image Schemas --- #
class ImageBase(BaseModel):
    image_url: HttpUrl = Field(..., description="Valid URL for the image")

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: str
    hospital_id: str
    uploaded_at: datetime

    model_config = {"from_attributes": True}


# --- Hospital Schemas --- #
class HospitalBase(BaseModel):
    organization_id: str = Field(..., description="UUID of the owning organization")
    name: str = Field(..., min_length=2, max_length=255, examples=["City General Hospital"])
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = Field(None, max_length=150)
    state: Optional[str] = Field(None, max_length=150)
    country: Optional[str] = Field(None, max_length=150)
    postal_code: Optional[str] = Field(None, max_length=20)
    
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    is_active: bool = True

class HospitalCreate(HospitalBase):
    facilities: Optional[List[FacilityCreate]] = []
    images: Optional[List[ImageCreate]] = []

class HospitalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = Field(None, max_length=150)
    state: Optional[str] = Field(None, max_length=150)
    country: Optional[str] = Field(None, max_length=150)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    is_active: Optional[bool] = None

class HospitalResponse(HospitalBase):
    id: str
    rating: float
    total_reviews: int
    created_at: datetime
    updated_at: datetime
    
    facilities: List[FacilityResponse] = []
    images: List[ImageResponse] = []

    model_config = {"from_attributes": True}

# --- Generic API Response Wrappers --- #
class PaginatedHospitalResponse(BaseModel):
    success: bool = True
    message: str = "operation successful"
    data: List[HospitalResponse]
    total: int
    page: int
    limit: int

class SingleHospitalResponse(BaseModel):
    success: bool = True
    message: str = "operation successful"
    data: HospitalResponse
