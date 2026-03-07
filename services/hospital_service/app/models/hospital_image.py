from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from services.hospital_service.app.db.base_model import BaseModel

class HospitalImage(BaseModel):
    __tablename__ = "hospital_images"

    hospital_id: Mapped[str] = mapped_column(String(36), ForeignKey('hospitals.id', ondelete="CASCADE"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    hospital: Mapped["Hospital"] = relationship("Hospital", back_populates="images")

    def __repr__(self):
        return f"<HospitalImage url='{self.image_url}'>"
