from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from services.doctor_service.app.models.doctor_kyc import KYCStatus


class KYCBase(BaseModel):
    aadhaar_number: Optional[str] = Field(None, min_length=12, max_length=12, examples=["123456789012"])
    pan_number: Optional[str] = Field(None, min_length=10, max_length=10, examples=["ABCDE1234F"])


class KYCResponse(BaseModel):
    id: str
    doctor_id: str
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_document_url: Optional[str] = None
    pan_document_url: Optional[str] = None
    selfie_url: Optional[str] = None
    kyc_status: KYCStatus
    reject_reason: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class KYCRejectRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500, examples=["Aadhaar number mismatch"])


class DoctorApproveRequest(BaseModel):
    notes: Optional[str] = Field(None, max_length=500)


class DoctorRejectRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500, examples=["Medical license is expired"])
