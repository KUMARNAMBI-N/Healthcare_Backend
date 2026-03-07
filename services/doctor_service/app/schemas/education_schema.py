from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EducationBase(BaseModel):
    degree: str
    university: str
    year_completed: int

class EducationCreate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: str
    doctor_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
