from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.doctor_service.app.db.base_model import BaseModel

class Experience(BaseModel):
    __tablename__ = "doctor_experience"

    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey('doctors.id', ondelete="CASCADE"), nullable=False)
    hospital_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(150), nullable=False)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)
    end_year: Mapped[int] = mapped_column(Integer, nullable=True)

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="experiences")
