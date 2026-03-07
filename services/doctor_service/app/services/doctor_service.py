from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.doctor_service.app.repository.doctor_repository import DoctorRepository
from services.doctor_service.app.schemas.doctor_schema import DoctorCreate, DoctorUpdate, DoctorResponse, DoctorProfileResponse
from services.doctor_service.app.schemas.education_schema import EducationCreate, EducationResponse
from services.doctor_service.app.schemas.experience_schema import ExperienceCreate, ExperienceResponse
from services.doctor_service.app.schemas.language_schema import LanguageCreate, LanguageResponse

class DoctorService:
    def __init__(self, db_session: AsyncSession):
        self.repository = DoctorRepository(db_session)

    async def create_doctor(self, doctor_in: DoctorCreate) -> DoctorResponse:
        # Business rule: prevent duplicate email for doctors
        existing_doctor = await self.repository.get_doctor_by_email(email=doctor_in.email)
        if existing_doctor:
            raise HTTPException(status_code=400, detail="A doctor with this email already exists.")
            
        try:
            doctor_db = await self.repository.create_doctor(doctor_in)
            return DoctorResponse.model_validate(doctor_db)
        except IntegrityError as e:
            await self.repository.session.rollback()
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e.orig)}")

    async def get_doctor(self, doctor_id: str) -> DoctorResponse:
        doctor_db = await self.repository.get_doctor_by_id(doctor_id)
        if not doctor_db:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorResponse.model_validate(doctor_db)

    async def get_doctor_profile(self, doctor_id: str) -> DoctorProfileResponse:
        doctor_db = await self.repository.get_full_doctor_profile(doctor_id)
        if not doctor_db:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorProfileResponse.model_validate(doctor_db)

    async def update_doctor(self, doctor_id: str, doctor_in: DoctorUpdate) -> DoctorResponse:
        doctor_db = await self.repository.update_doctor(doctor_id, doctor_in)
        if not doctor_db:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return DoctorResponse.model_validate(doctor_db)

    async def delete_doctor(self, doctor_id: str) -> dict:
        success = await self.repository.delete_doctor(doctor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return {"message": "Doctor deleted successfully"}

    async def list_doctors(self, filters: Dict[str, Any]) -> List[DoctorResponse]:
        doctors_db = await self.repository.list_doctors(**filters)
        return [DoctorResponse.model_validate(doc) for doc in doctors_db]

    async def add_education(self, doctor_id: str, edu_in: EducationCreate) -> EducationResponse:
        # Validate doctor exists
        await self.get_doctor(doctor_id)
        edu_db = await self.repository.add_education(doctor_id, edu_in)
        return EducationResponse.model_validate(edu_db)

    async def add_experience(self, doctor_id: str, exp_in: ExperienceCreate) -> ExperienceResponse:
        # Validate doctor exists
        await self.get_doctor(doctor_id)
        exp_db = await self.repository.add_experience(doctor_id, exp_in)
        return ExperienceResponse.model_validate(exp_db)

    async def add_language(self, doctor_id: str, lang_in: LanguageCreate) -> LanguageResponse:
        # Validate doctor exists
        await self.get_doctor(doctor_id)
        lang_db = await self.repository.add_language(doctor_id, lang_in)
        return LanguageResponse.model_validate(lang_db)
