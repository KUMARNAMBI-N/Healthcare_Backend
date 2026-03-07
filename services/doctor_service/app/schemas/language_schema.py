from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LanguageBase(BaseModel):
    language: str

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    id: str
    doctor_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
