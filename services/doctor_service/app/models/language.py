from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.doctor_service.app.db.base_model import BaseModel

class Language(BaseModel):
    __tablename__ = "doctor_languages"

    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey('doctors.id', ondelete="CASCADE"), nullable=False)
    language: Mapped[str] = mapped_column(String(100), nullable=False)

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="languages")
