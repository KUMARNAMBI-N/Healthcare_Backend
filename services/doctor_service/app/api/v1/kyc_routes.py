from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from services.doctor_service.app.db.session import get_db_session
from services.doctor_service.app.repository.doctor_repository import DoctorRepository
from services.doctor_service.app.repository.kyc_repository import KYCRepository
from services.doctor_service.app.schemas.kyc_schema import KYCResponse, KYCRejectRequest
from services.doctor_service.app.models.doctor import ApprovalStatus
from services.doctor_service.app.core.file_storage import save_upload

router = APIRouter()


def get_repos(db: AsyncSession = Depends(get_db_session)):
    return {
        "doctor": DoctorRepository(db),
        "kyc": KYCRepository(db),
    }


async def _require_approved_doctor(doctor_id: str, repos: dict):
    doctor = await repos["doctor"].get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if doctor.approval_status != ApprovalStatus.approved:
        raise HTTPException(
            status_code=403,
            detail=f"Doctor profile must be approved before submitting KYC. "
                   f"Current status: {doctor.approval_status}"
        )
    return doctor


# ─── KYC Submission ───────────────────────────────────────────────────────────

@router.post("/{doctor_id}/kyc", response_model=KYCResponse, status_code=status.HTTP_201_CREATED)
async def submit_kyc(
    doctor_id: str,
    aadhaar_number: Optional[str] = Form(None, description="12-digit Aadhaar number"),
    pan_number: Optional[str] = Form(None, description="10-character PAN number"),
    aadhaar_document: Optional[UploadFile] = File(None, description="Aadhaar card PDF or image"),
    pan_document: Optional[UploadFile] = File(None, description="PAN card PDF or image"),
    selfie: Optional[UploadFile] = File(None, description="Recent face photo of the doctor"),
    repos: dict = Depends(get_repos),
):
    """
    Doctor submits KYC documents (Aadhaar, PAN, selfie).
    **Doctor profile must be approved first.**
    """
    await _require_approved_doctor(doctor_id, repos)

    aadhaar_url = None
    pan_url = None
    selfie_url = None

    if aadhaar_document:
        aadhaar_url, _ = await save_upload(aadhaar_document, subfolder=f"doctor_kyc/{doctor_id}")
    if pan_document:
        pan_url, _ = await save_upload(pan_document, subfolder=f"doctor_kyc/{doctor_id}")
    if selfie:
        selfie_url, _ = await save_upload(selfie, subfolder=f"doctor_kyc/{doctor_id}")

    kyc = await repos["kyc"].submit_kyc(
        doctor_id=doctor_id,
        aadhaar_number=aadhaar_number,
        pan_number=pan_number,
        aadhaar_url=aadhaar_url,
        pan_url=pan_url,
        selfie_url=selfie_url,
    )
    return kyc


@router.get("/{doctor_id}/kyc", response_model=KYCResponse)
async def get_kyc_status(doctor_id: str, repos: dict = Depends(get_repos)):
    """Get the KYC submission status for a doctor."""
    doctor = await repos["doctor"].get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    kyc = await repos["kyc"].get_by_doctor_id(doctor_id)
    if not kyc:
        raise HTTPException(status_code=404, detail="No KYC submission found. Please submit KYC documents first.")
    return kyc


# ─── Admin KYC Review ─────────────────────────────────────────────────────────

@router.post("/{doctor_id}/kyc/approve", response_model=KYCResponse)
async def approve_kyc(doctor_id: str, repos: dict = Depends(get_repos)):
    """
    Admin: Approve a doctor's KYC documents.
    After approval, the doctor is fully verified on the platform.
    """
    kyc = await repos["kyc"].get_by_doctor_id(doctor_id)
    if not kyc:
        raise HTTPException(status_code=404, detail="No KYC submission found for this doctor.")
    if kyc.kyc_status.value == "approved":
        raise HTTPException(status_code=400, detail="KYC is already approved.")
    return await repos["kyc"].approve(kyc)


@router.post("/{doctor_id}/kyc/reject", response_model=KYCResponse)
async def reject_kyc(
    doctor_id: str,
    body: KYCRejectRequest,
    repos: dict = Depends(get_repos)
):
    """Admin: Reject a doctor's KYC with a reason. The doctor can resubmit."""
    kyc = await repos["kyc"].get_by_doctor_id(doctor_id)
    if not kyc:
        raise HTTPException(status_code=404, detail="No KYC submission found for this doctor.")
    return await repos["kyc"].reject(kyc, body.reason)
