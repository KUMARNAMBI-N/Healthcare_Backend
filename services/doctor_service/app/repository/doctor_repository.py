from typing import List, Optional, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload

from services.doctor_service.app.models.doctor import Doctor
from services.doctor_service.app.models.education import Education
from services.doctor_service.app.models.experience import Experience
from services.doctor_service.app.models.language import Language
from services.doctor_service.app.models.document import Document
from services.doctor_service.app.schemas.doctor_schema import DoctorCreate, DoctorUpdate
from services.doctor_service.app.schemas.education_schema import EducationCreate
from services.doctor_service.app.schemas.experience_schema import ExperienceCreate
from services.doctor_service.app.schemas.language_schema import LanguageCreate

class DoctorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_doctor(self, doctor_in: DoctorCreate) -> Doctor:
        db_obj = Doctor(**doctor_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        query = select(Doctor).where(Doctor.id == doctor_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
        
    async def get_doctor_by_email(self, email: str) -> Optional[Doctor]:
        query = select(Doctor).where(Doctor.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_full_doctor_profile(self, doctor_id: str) -> Optional[Doctor]:
        query = select(Doctor).where(Doctor.id == doctor_id).options(
            selectinload(Doctor.educations),
            selectinload(Doctor.experiences),
            selectinload(Doctor.languages),
            selectinload(Doctor.documents)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_doctor(self, doctor_id: str, doctor_update: DoctorUpdate) -> Optional[Doctor]:
        doctor = await self.get_doctor_by_id(doctor_id)
        if not doctor:
            return None
        
        update_data = doctor_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(doctor, field, value)
            
        await self.session.commit()
        await self.session.refresh(doctor)
        return doctor

    async def delete_doctor(self, doctor_id: str) -> bool:
        doctor = await self.get_doctor_by_id(doctor_id)
        if not doctor:
            return False
            
        await self.session.delete(doctor)
        await self.session.commit()
        return True

    async def list_doctors(self, 
                           specialization_id: Optional[str] = None, 
                           hospital_id: Optional[str] = None,
                           min_experience: Optional[int] = None,
                           rating: Optional[float] = None,
                           skip: int = 0, 
                           limit: int = 100) -> List[Doctor]:
        
        query = select(Doctor).where(Doctor.is_active == True)
        
        if specialization_id:
            query = query.where(Doctor.specialization_id == specialization_id)
        if hospital_id:
            query = query.where(Doctor.hospital_id == hospital_id)
        if min_experience is not None:
            query = query.where(Doctor.experience_years >= min_experience)
        if rating is not None:
            query = query.where(Doctor.rating >= rating)
            
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    # Nested entity creation logic
    async def add_education(self, doctor_id: str, edu_in: EducationCreate) -> Education:
        db_obj = Education(doctor_id=doctor_id, **edu_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def add_experience(self, doctor_id: str, exp_in: ExperienceCreate) -> Experience:
        db_obj = Experience(doctor_id=doctor_id, **exp_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def add_language(self, doctor_id: str, lang_in: LanguageCreate) -> Language:
        db_obj = Language(doctor_id=doctor_id, **lang_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
