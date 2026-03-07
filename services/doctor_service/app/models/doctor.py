from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, CheckConstraint, DECIMAL, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import List
from services.doctor_service.app.db.base_model import BaseModel

class Doctor(BaseModel):
    __tablename__ = "doctors"

    hospital_id: Mapped[str] = mapped_column(String(36), index=True, nullable=True)
    organization_id: Mapped[str] = mapped_column(String(36), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    specialization_id: Mapped[str] = mapped_column(String(36), ForeignKey('doctor_specializations.id'), index=True, nullable=True)
    qualification: Mapped[str] = mapped_column(Text, nullable=True)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    consultation_fee: Mapped[float] = mapped_column(DECIMAL, nullable=False, default=0.0)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_image: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[float] = mapped_column(DECIMAL, index=True, server_default=text("0"))
    total_reviews: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    __table_args__ = (
        CheckConstraint('experience_years >= 0', name='check_experience_positive'),
        CheckConstraint('consultation_fee >= 0', name='check_fee_positive'),
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_range'),
    )

    specialization: Mapped["Specialization"] = relationship("Specialization", back_populates="doctors")
    educations: Mapped[List["Education"]] = relationship("Education", back_populates="doctor", cascade="all, delete-orphan")
    experiences: Mapped[List["Experience"]] = relationship("Experience", back_populates="doctor", cascade="all, delete-orphan")
    languages: Mapped[List["Language"]] = relationship("Language", back_populates="doctor", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="doctor", cascade="all, delete-orphan")
    hospitals: Mapped[List["DoctorHospital"]] = relationship("DoctorHospital", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Doctor name='{self.full_name}' email='{self.email}'>"
