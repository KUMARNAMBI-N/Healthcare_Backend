from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List

from services.doctor_service.app.db.session import get_db_session
from services.doctor_service.app.repository.specialization_repository import SpecializationRepository
from services.doctor_service.app.schemas.specialization_schema import (
    SpecializationCreate, SpecializationUpdate, SpecializationResponse
)

router = APIRouter()


def get_spec_repo(db: AsyncSession = Depends(get_db_session)) -> SpecializationRepository:
    return SpecializationRepository(db)


@router.post("/", response_model=SpecializationResponse, status_code=status.HTTP_201_CREATED)
async def create_specialization(
    spec_in: SpecializationCreate,
    repo: SpecializationRepository = Depends(get_spec_repo)
):
    """Create a new specialization (e.g. Cardiology, Dermatology)."""
    existing = await repo.get_by_name(spec_in.name)
    if existing:
        raise HTTPException(status_code=400, detail=f"Specialization '{spec_in.name}' already exists.")
    try:
        return await repo.create(spec_in)
    except IntegrityError as e:
        await repo.session.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e.orig)}")


@router.get("/", response_model=List[SpecializationResponse])
async def list_specializations(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    repo: SpecializationRepository = Depends(get_spec_repo)
):
    """List all available specializations."""
    skip = (page - 1) * limit
    return await repo.list_all(skip=skip, limit=limit)


@router.get("/{spec_id}", response_model=SpecializationResponse)
async def get_specialization(spec_id: str, repo: SpecializationRepository = Depends(get_spec_repo)):
    """Get a single specialization by ID."""
    spec = await repo.get_by_id(spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return spec


@router.put("/{spec_id}", response_model=SpecializationResponse)
async def update_specialization(
    spec_id: str,
    spec_update: SpecializationUpdate,
    repo: SpecializationRepository = Depends(get_spec_repo)
):
    """Update an existing specialization."""
    spec = await repo.update(spec_id, spec_update)
    if not spec:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return spec


@router.delete("/{spec_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specialization(spec_id: str, repo: SpecializationRepository = Depends(get_spec_repo)):
    """Delete a specialization."""
    success = await repo.delete(spec_id)
    if not success:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return None
