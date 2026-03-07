from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.hospital_service.app.db.base_model import BaseModel

class HospitalFacility(BaseModel):
    __tablename__ = "hospital_facilities"

    hospital_id: Mapped[str] = mapped_column(String(36), ForeignKey('hospitals.id', ondelete="CASCADE"), nullable=False, index=True)
    facility_name: Mapped[str] = mapped_column(String(255), nullable=False)

    hospital: Mapped["Hospital"] = relationship("Hospital", back_populates="facilities")

    def __repr__(self):
        return f"<HospitalFacility name='{self.facility_name}'>"
