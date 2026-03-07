from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SpecializationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, examples=["Cardiology"])
    description: Optional[str] = Field(None, examples=["Heart Treatment"])


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None


class SpecializationResponse(SpecializationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
