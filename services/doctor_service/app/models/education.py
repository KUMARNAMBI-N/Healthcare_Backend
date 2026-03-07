from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.doctor_service.app.db.base_model import BaseModel

class Education(BaseModel):
    __tablename__ = "doctor_education"

    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey('doctors.id', ondelete="CASCADE"), nullable=False)
    degree: Mapped[str] = mapped_column(String(150), nullable=False)
    university: Mapped[str] = mapped_column(String(255), nullable=False)
    year_completed: Mapped[int] = mapped_column(Integer, nullable=False)

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="educations")
