from services.doctor_service.app.schemas.doctor_schema import (
    DoctorBase, DoctorCreate, DoctorUpdate, DoctorResponse, DoctorProfileResponse
)
# Re-exported everything to handle the circular references in doctor_schema.py from my earlier mistake.
