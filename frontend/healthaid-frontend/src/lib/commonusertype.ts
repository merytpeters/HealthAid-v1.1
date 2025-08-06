interface EmergencyContact {
    name: string;
    email?: string;
}


export interface PersonalInfo {
    full_name: string;
    email: string;
    phone_number?: string;
    emergency_contact?: EmergencyContact;
}

export interface BioData {
    gender: string;
    age: number;
    weight?: number;
    height?: number;
    dob: string;
    blood_type?: string;
    bmi?: Float32Array;
}

export interface MenstrualCycleTracker {
    cycle_day?: number;
    period_start_date?: string;
    period_end_date?: string;
    symptoms?: string[];
}

export interface Hydration {
    amount_liters?: number;
    goal_liters?: number;
    hydration_status?: string;
}

export type MoodEnum = "happy" | "sad" | "anxious" | "neutral" | "stressed";

export interface MoodTracker {
    mood: MoodEnum;
    notes?: string;
}

export interface AlertWarnings {
    alerts: string[];
}

export interface HealthMetrics {
    heart_rate?: number;
    blood_pressure?: number;
    blood_glucose?: number;
    sleep_quality?: string;
    body_temperature?: number;
    respiratory_rate?: number;
    menstrual_cycle_tracker?: MenstrualCycleTracker;
    hydration?: Hydration;
    mood_tracker?: MoodTracker;
    alert_warnings?: AlertWarnings;
}
