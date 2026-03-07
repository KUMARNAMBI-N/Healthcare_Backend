from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.doctor_service.app.models.specialization import Specialization
from services.doctor_service.app.schemas.specialization_schema import SpecializationCreate, SpecializationUpdate


class SpecializationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, spec_in: SpecializationCreate) -> Specialization:
        db_obj = Specialization(**spec_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, spec_id: str) -> Optional[Specialization]:
        result = await self.session.execute(
            select(Specialization).where(Specialization.id == spec_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Specialization]:
        result = await self.session.execute(
            select(Specialization).where(Specialization.name == name)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Specialization]:
        result = await self.session.execute(
            select(Specialization).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, spec_id: str, spec_update: SpecializationUpdate) -> Optional[Specialization]:
        spec = await self.get_by_id(spec_id)
        if not spec:
            return None
        for field, value in spec_update.model_dump(exclude_unset=True).items():
            setattr(spec, field, value)
        await self.session.commit()
        await self.session.refresh(spec)
        return spec

    async def delete(self, spec_id: str) -> bool:
        spec = await self.get_by_id(spec_id)
        if not spec:
            return False
        await self.session.delete(spec)
        await self.session.commit()
        return True
