from sqlalchemy import String, Boolean, ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from services.doctor_service.app.db.base_model import BaseModel

class Document(BaseModel):
    __tablename__ = "doctor_documents"

    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey('doctors.id', ondelete="CASCADE"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False)
    document_url: Mapped[str] = mapped_column(Text, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    uploaded_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="documents")
