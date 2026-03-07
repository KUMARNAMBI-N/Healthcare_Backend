from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple

from services.hospital_service.app.models.hospital import Hospital
from services.hospital_service.app.models.hospital_facility import HospitalFacility
from services.hospital_service.app.models.hospital_image import HospitalImage

class HospitalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_hospital(self, hospital: Hospital) -> Hospital:
        self.session.add(hospital)
        await self.session.flush()
        return hospital
        
    async def add_facility(self, facility: HospitalFacility):
        self.session.add(facility)

    async def add_image(self, image: HospitalImage):
        self.session.add(image)

    async def get_by_id(self, hospital_id: str) -> Optional[Hospital]:
        result = await self.session.execute(
            select(Hospital)
            .options(selectinload(Hospital.facilities), selectinload(Hospital.images))
            .where(Hospital.id == hospital_id)
        )
        return result.scalar_one_or_none()

    async def update(self, hospital: Hospital) -> Hospital:
        await self.session.flush()
        return hospital

    async def delete(self, hospital_id: str) -> bool:
        hospital = await self.get_by_id(hospital_id)
        if hospital:
            await self.session.delete(hospital)
            await self.session.flush()
            return True
        return False

    async def list_hospitals(
        self,
        skip: int = 0,
        limit: int = 10,
        city: Optional[str] = None,
        rating: Optional[float] = None,
        organization_id: Optional[str] = None
    ) -> Tuple[List[Hospital], int]:
        filters = []
        if city:
            filters.append(Hospital.city.ilike(f"%{city}%"))
        if rating is not None:
            filters.append(Hospital.rating >= rating)
        if organization_id:
            filters.append(Hospital.organization_id == organization_id)
            
        stmt = select(Hospital).options(selectinload(Hospital.facilities), selectinload(Hospital.images))
        count_stmt = select(func.count(Hospital.id))
        
        if filters:
            stmt = stmt.where(and_(*filters))
            count_stmt = count_stmt.where(and_(*filters))
            
        stmt = stmt.offset(skip).limit(limit)
        
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def find_nearby(self, lat: float, lng: float, radius_km: float) -> List[Hospital]:
        """
        Uses the Haversine formula natively in PostgeSQL to find hospitals within radius_km.
        Earth radius is approx 6371 km.
        """
        # ACOS(SIN(lat1)*SIN(lat2)+COS(lat1)*COS(lat2)*COS(lon2-lon1))*6371
        
        haversine_formula = (
            6371 * func.acos(
                func.cos(func.radians(lat)) * func.cos(func.radians(Hospital.latitude)) *
                func.cos(func.radians(Hospital.longitude) - func.radians(lng)) +
                func.sin(func.radians(lat)) * func.sin(func.radians(Hospital.latitude))
            )
        )
        
        stmt = (
            select(Hospital)
            .options(selectinload(Hospital.facilities), selectinload(Hospital.images))
            .where(haversine_formula <= radius_km)
            .order_by(haversine_formula.asc())
        )
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
