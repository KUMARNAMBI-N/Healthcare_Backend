from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List, Optional

from services.hospital_service.app.repository.hospital_repository import HospitalRepository
from services.hospital_service.app.models.hospital import Hospital
from services.hospital_service.app.models.hospital_facility import HospitalFacility
from services.hospital_service.app.models.hospital_image import HospitalImage
from services.hospital_service.app.schemas.hospital_schema import (
    HospitalCreate, HospitalUpdate, 
    PaginatedHospitalResponse, SingleHospitalResponse, HospitalResponse
)
from services.hospital_service.app.core.logger import logger

class HospitalService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = HospitalRepository(session)

    async def create_hospital(self, hospital_data: HospitalCreate) -> SingleHospitalResponse:
        logger.info(f"Creating hospital: {hospital_data.name} for org: {hospital_data.organization_id}")
        
        data_dict = hospital_data.model_dump(exclude={"facilities", "images"})
        new_hospital = Hospital(**data_dict)
        
        await self.repository.create_hospital(new_hospital)
        
        # Add facilities if present
        if hospital_data.facilities:
            for fac in hospital_data.facilities:
                fac_model = HospitalFacility(hospital_id=new_hospital.id, facility_name=fac.facility_name)
                await self.repository.add_facility(fac_model)
                
        # Add images if present
        if hospital_data.images:
            for img in hospital_data.images:
                img_model = HospitalImage(hospital_id=new_hospital.id, image_url=str(img.image_url))
                await self.repository.add_image(img_model)
                
        # Commit to save relations
        await self.session.commit()
        
        # Need to fetch again to load relationships
        loaded_hospital = await self.repository.get_by_id(new_hospital.id)
        
        return SingleHospitalResponse(
            data=HospitalResponse.model_validate(loaded_hospital)
        )

    async def get_hospital(self, hospital_id: str) -> SingleHospitalResponse:
        hospital = await self.repository.get_by_id(hospital_id)
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
            
        return SingleHospitalResponse(
            data=HospitalResponse.model_validate(hospital)
        )

    async def update_hospital(self, hospital_id: str, update_data: HospitalUpdate) -> SingleHospitalResponse:
        hospital = await self.repository.get_by_id(hospital_id)
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
            
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(hospital, key, value)
            
        await self.repository.update(hospital)
        await self.session.commit()
        
        return SingleHospitalResponse(
            data=HospitalResponse.model_validate(hospital)
        )

    async def delete_hospital(self, hospital_id: str):
        success = await self.repository.delete(hospital_id)
        if not success:
            raise HTTPException(status_code=404, detail="Hospital not found")
        await self.session.commit()
        return {"success": True, "message": "Hospital deleted successfully"}

    async def list_hospitals(
        self, page: int, limit: int, city: Optional[str], rating: Optional[float], organization_id: Optional[str]
    ) -> PaginatedHospitalResponse:
        skip = (page - 1) * limit
        hospitals, total = await self.repository.list_hospitals(
            skip=skip, limit=limit, city=city, rating=rating, organization_id=organization_id
        )
        
        dtos = [HospitalResponse.model_validate(h) for h in hospitals]
        return PaginatedHospitalResponse(
            data=dtos,
            total=total,
            page=page,
            limit=limit
        )

    async def find_nearby(self, lat: float, lng: float, radius_km: float):
        hospitals = await self.repository.find_nearby(lat, lng, radius_km)
        dtos = [HospitalResponse.model_validate(h) for h in hospitals]
        return {
            "success": True,
            "message": "operation successful",
            "data": dtos
        }
