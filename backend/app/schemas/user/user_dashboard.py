"""Schema for Individual User Dashboard"""
from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List


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


class BioData(BaseModel):
    """BioData Schema"""
    gender: str
    age: int
    weight: Optional[float] = None
    height: Optional[float] = None
    dob: str
    blood_type: Optional[str] = None
    bmi: Optional[float] = None


class MenstrualCycleTracker(BaseModel):
    """Menstruation Schema"""
    cycle_day: Optional[int] = None
    period_start_date: Optional[date] = None
    period_end_date: Optional[date] = None
    symptoms: Optional[List[str]] = None


class Hydration(BaseModel):
    """Hydration tracker Schema"""
    amount_liters: Optional[float] = None
    goal_liters: Optional[float] = None
    hydration_status: Optional[str] = None  # e.g. "adequate", "low"


class MoodEnum(str, Enum):
    """Mood Schema"""
    happy = "happy"
    sad = "sad"
    anxious = "anxious"
    neutral = "neutral"
    stressed = "stressed"


class MoodTracker(BaseModel):
    """Mood Tracker Schema"""
    mood: MoodEnum
    notes: Optional[str] = None


class AlertWarnings(BaseModel):
    """Alerts and Warnings"""
    alerts: List[str] = []


class HealthMetrics(BaseModel):
    """Health Metrics"""
    heart_rate: Optional[float] = None
    blood_pressure: Optional[str] = None
    blood_glucose: Optional[float] = None
    sleep_quality: Optional[str] = None
    body_temperature: Optional[float] = None
    respiratory_rate: Optional[float] = None
    menstrual_cycle_tracker: Optional[MenstrualCycleTracker] = None
    hydration: Optional[Hydration] = None
    mood_tracker: Optional[MoodTracker] = None
    alert_warnings: Optional[AlertWarnings] = None
    
    
class UserDashboardCreate(BaseModel):
    """Schema to Create User Dashboard"""
    personal_info: PersonalInfo
    bio_data: BioData
    health_metrics: HealthMetrics
