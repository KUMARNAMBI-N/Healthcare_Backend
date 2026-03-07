from sqlalchemy import String, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.doctor_service.app.db.base_model import BaseModel

class DoctorHospital(BaseModel):
    __tablename__ = "doctor_hospitals"

    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey('doctors.id', ondelete="CASCADE"), nullable=False)
    hospital_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    consultation_fee: Mapped[float] = mapped_column(DECIMAL, nullable=False, default=0.0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="hospitals")
