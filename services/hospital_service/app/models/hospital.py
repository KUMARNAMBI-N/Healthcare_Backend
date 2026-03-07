from sqlalchemy import String, Text, Boolean, Integer, DECIMAL, text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from services.hospital_service.app.db.base_model import BaseModel

class Hospital(BaseModel):
    __tablename__ = "hospitals"

    organization_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    
    address_line1: Mapped[str] = mapped_column(Text, nullable=True)
    address_line2: Mapped[str] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(150), index=True, nullable=True)
    state: Mapped[str] = mapped_column(String(150), nullable=True)
    country: Mapped[str] = mapped_column(String(150), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    
    latitude: Mapped[float] = mapped_column(Float(53), index=True, nullable=True)
    longitude: Mapped[float] = mapped_column(Float(53), index=True, nullable=True)
    
    rating: Mapped[float] = mapped_column(DECIMAL, index=True, server_default=text("0"))
    total_reviews: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    facilities: Mapped[List["HospitalFacility"]] = relationship(
        "HospitalFacility", back_populates="hospital", cascade="all, delete-orphan"
    )
    images: Mapped[List["HospitalImage"]] = relationship(
        "HospitalImage", back_populates="hospital", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Hospital name='{self.name}' city='{self.city}'>"
