from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from services.doctor_service.app.models.doctor_license import DoctorLicense, LicenseStatus
from services.doctor_service.app.schemas.license_schema import LicenseRejectRequest


class LicenseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_or_replace(
        self, doctor_id: str, license_number: str,
        document_url: str, document_type: str,
        issuing_authority: Optional[str] = None,
        issue_date=None, expiry_date=None
    ) -> DoctorLicense:
        # If a license already exists for this doctor, delete it first
        existing = await self.get_by_doctor_id(doctor_id)
        if existing:
            await self.session.delete(existing)
            await self.session.commit()

        obj = DoctorLicense(
            doctor_id=doctor_id,
            license_number=license_number,
            license_document_url=document_url,
            license_document_type=document_type,
            issuing_authority=issuing_authority,
            issue_date=issue_date,
            expiry_date=expiry_date,
            status=LicenseStatus.pending_review
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_doctor_id(self, doctor_id: str) -> Optional[DoctorLicense]:
        result = await self.session.execute(
            select(DoctorLicense).where(DoctorLicense.doctor_id == doctor_id)
        )
        return result.scalar_one_or_none()

    async def approve(self, license: DoctorLicense) -> DoctorLicense:
        license.status = LicenseStatus.approved
        license.reject_reason = None
        await self.session.commit()
        await self.session.refresh(license)
        return license

    async def reject(self, license: DoctorLicense, reason: str) -> DoctorLicense:
        license.status = LicenseStatus.rejected
        license.reject_reason = reason
        await self.session.commit()
        await self.session.refresh(license)
        return license
