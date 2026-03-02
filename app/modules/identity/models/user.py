from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.base_model import BaseModel
from app.constants import STATUS_ACTIVE, STATUS_INACTIVE, STATUS_BANNED, ROLES

class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50), default=STATUS_ACTIVE)
    role: Mapped[str] = mapped_column(String(50), default=ROLES["PATIENT"])

    def __repr__(self):
        return f"<User {self.email}>"
