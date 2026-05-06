"""Schema for Individual User Dashboard"""

from typing import Optional

from pydantic import BaseModel, EmailStr

from app.api.v1.dashboards.schemas.dashboard_health_metrics_schema import (
    BioData,
    HealthMetrics,
)


class EmergencyContact(BaseModel):
    """Emergency Contact"""

    name: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None


class PersonalInfo(BaseModel):
    """Personal Info Schema"""

    full_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    emergency_contact: Optional[EmergencyContact] = None


class UserDashboardCreate(BaseModel):
    """Schema to Create User Dashboard"""

    personal_info: PersonalInfo
    bio_data: BioData
    health_metrics: HealthMetrics
