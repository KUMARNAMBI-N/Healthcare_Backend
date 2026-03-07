from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

from services.doctor_service.app.db.session import get_db_session
from services.doctor_service.app.repository.doctor_repository import DoctorRepository
from services.doctor_service.app.repository.license_repository import LicenseRepository
from services.doctor_service.app.repository.kyc_repository import KYCRepository
from services.doctor_service.app.schemas.license_schema import LicenseResponse, LicenseRejectRequest
from services.doctor_service.app.schemas.kyc_schema import DoctorApproveRequest, DoctorRejectRequest
from services.doctor_service.app.schemas.doctor_schema import DoctorResponse
from services.doctor_service.app.models.doctor import ApprovalStatus
from services.doctor_service.app.core.file_storage import save_upload
from datetime import datetime, timezone

router = APIRouter()


def get_repos(db: AsyncSession = Depends(get_db_session)):
    return {
        "doctor": DoctorRepository(db),
        "license": LicenseRepository(db),
    }


async def _require_doctor(doctor_id: str, repos: dict):
    doctor = await repos["doctor"].get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ─── License Upload ──────────────────────────────────────────────────────────

@router.post("/{doctor_id}/license", response_model=LicenseResponse, status_code=status.HTTP_201_CREATED)
async def upload_license(
    doctor_id: str,
    license_number: str = Form(..., description="Medical license number e.g. MCI-123456"),
    issuing_authority: Optional[str] = Form(None, description="e.g. Medical Council of India"),
    issue_date: Optional[date] = Form(None),
    expiry_date: Optional[date] = Form(None),
    license_file: UploadFile = File(..., description="Upload license as PDF or image (JPG/PNG)"),
    repos: dict = Depends(get_repos),
):
    """
    Upload a medical license PDF or image for a doctor.
    The license will be set to **pending_review** status.
    """
    await _require_doctor(doctor_id, repos)

    document_url, document_type = await save_upload(license_file, subfolder=f"doctor_license/{doctor_id}")

    lic = await repos["license"].create_or_replace(
        doctor_id=doctor_id,
        license_number=license_number,
        document_url=document_url,
        document_type=document_type,
        issuing_authority=issuing_authority,
        issue_date=issue_date,
        expiry_date=expiry_date,
    )
    return lic


@router.get("/{doctor_id}/license", response_model=LicenseResponse)
async def get_license(doctor_id: str, repos: dict = Depends(get_repos)):
    """Get the medical license details for a doctor."""
    await _require_doctor(doctor_id, repos)
    lic = await repos["license"].get_by_doctor_id(doctor_id)
    if not lic:
        raise HTTPException(status_code=404, detail="No license found for this doctor. Please upload one first.")
    return lic


# ─── Admin License Review ─────────────────────────────────────────────────────

@router.post("/{doctor_id}/license/approve", response_model=LicenseResponse)
async def approve_license(doctor_id: str, repos: dict = Depends(get_repos)):
    """Admin: Approve a doctor's uploaded medical license."""
    await _require_doctor(doctor_id, repos)
    lic = await repos["license"].get_by_doctor_id(doctor_id)
    if not lic:
        raise HTTPException(status_code=404, detail="No license uploaded by this doctor.")
    return await repos["license"].approve(lic)


@router.post("/{doctor_id}/license/reject", response_model=LicenseResponse)
async def reject_license(
    doctor_id: str,
    body: LicenseRejectRequest,
    repos: dict = Depends(get_repos)
):
    """Admin: Reject a doctor's medical license with a reason."""
    await _require_doctor(doctor_id, repos)
    lic = await repos["license"].get_by_doctor_id(doctor_id)
    if not lic:
        raise HTTPException(status_code=404, detail="No license uploaded by this doctor.")
    return await repos["license"].reject(lic, body.reason)


# ─── Doctor Profile Approval ──────────────────────────────────────────────────

@router.post("/{doctor_id}/approve", response_model=DoctorResponse)
async def approve_doctor(
    doctor_id: str,
    body: DoctorApproveRequest,
    repos: dict = Depends(get_repos)
):
    """
    Admin: Approve a doctor's profile, allowing them to submit KYC.
    """
    doctor = await _require_doctor(doctor_id, repos)
    if doctor.approval_status == ApprovalStatus.approved:
        raise HTTPException(status_code=400, detail="Doctor is already approved.")

    doctor.approval_status = ApprovalStatus.approved
    doctor.approved_at = datetime.now(timezone.utc)
    doctor.approved_by = "admin"  # Replace with real admin user ID from JWT
    await repos["doctor"].session.commit()
    await repos["doctor"].session.refresh(doctor)
    return DoctorResponse.model_validate(doctor)


@router.post("/{doctor_id}/reject", response_model=DoctorResponse)
async def reject_doctor(
    doctor_id: str,
    body: DoctorRejectRequest,
    repos: dict = Depends(get_repos)
):
    """Admin: Reject a doctor's profile registration with a reason."""
    doctor = await _require_doctor(doctor_id, repos)
    doctor.approval_status = ApprovalStatus.rejected
    doctor.approved_at = None
    doctor.approved_by = None
    await repos["doctor"].session.commit()
    await repos["doctor"].session.refresh(doctor)
    return DoctorResponse.model_validate(doctor)


@router.get("/pending", response_model=list[DoctorResponse])
async def list_pending_doctors(repos: dict = Depends(get_repos)):
    """Admin: List all doctors with pending approval status."""
    from sqlalchemy import select
    from services.doctor_service.app.models.doctor import Doctor
    result = await repos["doctor"].session.execute(
        select(Doctor).where(Doctor.approval_status == ApprovalStatus.pending)
    )
    doctors = list(result.scalars().all())
    return [DoctorResponse.model_validate(d) for d in doctors]
