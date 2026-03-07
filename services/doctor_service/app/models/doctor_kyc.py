import enum
from sqlalchemy import String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional
from services.doctor_service.app.db.base_model import BaseModel


class KYCStatus(str, enum.Enum):
    not_submitted = "not_submitted"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class DoctorKYC(BaseModel):
    __tablename__ = "doctor_kyc"

    doctor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    aadhaar_number: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    pan_number: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    aadhaar_document_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pan_document_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    selfie_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    kyc_status: Mapped[KYCStatus] = mapped_column(
        Enum(KYCStatus, name="kyc_status_enum"),
        default=KYCStatus.not_submitted,
        nullable=False
    )
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="kyc")
