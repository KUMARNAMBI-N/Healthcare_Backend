import enum
from sqlalchemy import String, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import Optional
from services.doctor_service.app.db.base_model import BaseModel


class LicenseStatus(str, enum.Enum):
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"


class DoctorLicense(BaseModel):
    __tablename__ = "doctor_licenses"

    doctor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    license_number: Mapped[str] = mapped_column(String(100), nullable=False)
    license_document_url: Mapped[str] = mapped_column(Text, nullable=False)
    license_document_type: Mapped[str] = mapped_column(String(10), nullable=False)  # pdf | image
    issuing_authority: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    issue_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[LicenseStatus] = mapped_column(
        Enum(LicenseStatus, name="license_status_enum"),
        default=LicenseStatus.pending_review,
        nullable=False
    )
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="license")
