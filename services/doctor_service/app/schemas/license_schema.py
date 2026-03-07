from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from services.doctor_service.app.models.doctor_license import LicenseStatus


class LicenseResponse(BaseModel):
    id: str
    doctor_id: str
    license_number: str
    license_document_url: str
    license_document_type: str
    issuing_authority: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: LicenseStatus
    reject_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LicenseApproveRequest(BaseModel):
    pass  # No body needed for approve


class LicenseRejectRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500, examples=["License number unverifiable"])
