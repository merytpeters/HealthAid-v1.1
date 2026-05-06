"""Schemas for Health Metrics"""

from datetime import date
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class BloodType(str, Enum):
    """Blood Type Enum"""

    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class GenoType(str, Enum):
    """Genotype Enum"""

    AA = "AA"
    AS = "AS"
    AC = "AC"
    SS = "SS"
    SC = "SC"


class Metric(BaseModel):
    """Metric Body"""

    value: float | int
    unit: Literal[
        "kg",
        "lb",  # Weight
        "cm",
        "m",
        "inch",
        "in",
        "ft",  # Height/length
        "bpm",  # Heart Rate
        "breaths/min",
        "brpm",  # Respiratory Rate
        "mg/dL",
        "mmol/L",  # Blood Glucose
        "degC",
        "degF",
        "K",  # Temperature
        "L",
        "ml",
        "gal",
        "floz",
        "cl",  # Liquid volume
    ]


class BioData(BaseModel):
    """BioData Schema"""

    gender: str
    age: int
    weight: Optional[Metric] = None
    height: Optional[Metric] = None
    dob: date
    blood_type: Optional[BloodType] = None
    genotype: Optional[GenoType] = None
    bmi: Optional[float] = Field(None, gt=10, lt=100)

    @field_validator("dob")
    @classmethod
    def check_not_in_future(cls, v):
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v


class MenstrualCycleTracker(BaseModel):
    """Menstruation Schema"""

    cycle_day: Optional[int] = None
    period_start_date: Optional[date] = None
    period_end_date: Optional[date] = None
    symptoms: Optional[List[str]] = None


class Hydration(BaseModel):
    """Hydration tracker Schema"""

    amount_liters: Optional[Metric] = None
    goal_liters: Optional[Metric] = None
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


class BloodPressure(BaseModel):
    """Blood pressure schema"""

    systolic: int = Field(..., gt=40, lt=250)
    diastolic: int = Field(..., gt=30, lt=150)
    unit: str = "mmHg"

    def __str__(self):
        """Blood Pressure string representation"""

        return f"{self.systolic}/{self.diastolic} {self.unit}"


class HealthMetrics(BaseModel):
    """Health Metrics"""

    heart_rate: Optional[Metric] = Field(None, gt=30, lt=250)
    blood_pressure: Optional[BloodPressure] = None
    blood_glucose: Optional[Metric] = None
    sleep_quality: Optional[str] = None
    body_temperature: Optional[Metric] = None
    respiratory_rate: Optional[Metric] = None
    menstrual_cycle_tracker: Optional[MenstrualCycleTracker] = None
    hydration: Optional[Hydration] = None
    mood_tracker: Optional[MoodTracker] = None
    alert_warnings: Optional[AlertWarnings] = None
