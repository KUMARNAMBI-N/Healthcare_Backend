from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ExperienceBase(BaseModel):
    hospital_name: str
    role: str
    start_year: int
    end_year: Optional[int] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceResponse(ExperienceBase):
    id: str
    doctor_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
