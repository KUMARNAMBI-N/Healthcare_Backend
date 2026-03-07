from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from services.doctor_service.app.models.doctor_kyc import DoctorKYC, KYCStatus


class KYCRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_doctor_id(self, doctor_id: str) -> Optional[DoctorKYC]:
        result = await self.session.execute(
            select(DoctorKYC).where(DoctorKYC.doctor_id == doctor_id)
        )
        return result.scalar_one_or_none()

    async def submit_kyc(
        self,
        doctor_id: str,
        aadhaar_number: Optional[str],
        pan_number: Optional[str],
        aadhaar_url: Optional[str],
        pan_url: Optional[str],
        selfie_url: Optional[str]
    ) -> DoctorKYC:
        existing = await self.get_by_doctor_id(doctor_id)
        if existing:
            # Update existing KYC submission
            existing.aadhaar_number = aadhaar_number or existing.aadhaar_number
            existing.pan_number = pan_number or existing.pan_number
            if aadhaar_url:
                existing.aadhaar_document_url = aadhaar_url
            if pan_url:
                existing.pan_document_url = pan_url
            if selfie_url:
                existing.selfie_url = selfie_url
            existing.kyc_status = KYCStatus.pending
            existing.reject_reason = None
            await self.session.commit()
            await self.session.refresh(existing)
            return existing

        obj = DoctorKYC(
            doctor_id=doctor_id,
            aadhaar_number=aadhaar_number,
            pan_number=pan_number,
            aadhaar_document_url=aadhaar_url,
            pan_document_url=pan_url,
            selfie_url=selfie_url,
            kyc_status=KYCStatus.pending
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def approve(self, kyc: DoctorKYC) -> DoctorKYC:
        kyc.kyc_status = KYCStatus.approved
        kyc.reject_reason = None
        kyc.verified_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(kyc)
        return kyc

    async def reject(self, kyc: DoctorKYC, reason: str) -> DoctorKYC:
        kyc.kyc_status = KYCStatus.rejected
        kyc.reject_reason = reason
        kyc.verified_at = None
        await self.session.commit()
        await self.session.refresh(kyc)
        return kyc
