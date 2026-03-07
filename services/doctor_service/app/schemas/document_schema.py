from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    document_type: str
    document_url: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    verified: Optional[bool] = None

class DocumentResponse(DocumentBase):
    id: str
    doctor_id: str
    verified: bool
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
