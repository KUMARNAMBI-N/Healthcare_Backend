from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from services.doctor_service.app.db.base_model import BaseModel

class Specialization(BaseModel):
    __tablename__ = "doctor_specializations"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    doctors: Mapped[List["Doctor"]] = relationship("Doctor", back_populates="specialization")
