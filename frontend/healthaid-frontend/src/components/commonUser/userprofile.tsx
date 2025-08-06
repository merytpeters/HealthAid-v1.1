import type {
    PersonalInfo,
    BioData,
    HealthMetrics
} from "../../lib/commonusertype";
import '../../styles/userdashboards/commonuserprofile.css'

interface ProfileProps {
  PersonalInfo: PersonalInfo;
}

export function Profile ({ PersonalInfo }: ProfileProps) {
  return (
	<div className="prof">
	  <div className="userInfo">
        <p>Name {PersonalInfo.full_name}</p>
        <p>Email: {PersonalInfo.email}</p>
       </div>
	  <div className="emergency">
		<p>
		  Emergency Contact: {PersonalInfo.emergency_contact
			? `${PersonalInfo.emergency_contact.name} (${PersonalInfo.emergency_contact.email})`
			: "Not provided"}
		</p>
	  </div>
	</div>
  );
}

interface BioProps {
    BioData: BioData
}

export function ProfileData ({ BioData }: BioProps) {
    return (
        <div className="profdata">
            <div className="bioinfo">
                <div className="row-one">
                   <p>Gender: {BioData.gender}</p>
                   <p>Age: {BioData.age}</p>
                   <p>Height: {BioData.height}</p>
                </div>
                <div className="row-two">
                   <p>Weight: {BioData.weight}</p>
                   <p>BMI: {BioData.bmi}</p>
                   <p>Blood Type: {BioData.blood_type}</p>
                </div>
            </div>
        </div>
    )
}

interface HealthMetricsProps {
    HealthMetrics: HealthMetrics
}

export function HealthMetricsData ({ HealthMetrics }: HealthMetricsProps) {
    return (
        <div className="healthdata">
            <div className="healthInfo">
                <p>Heart Rate: {HealthMetrics.heart_rate ?? "N/A"}</p>
                <p>Blood Pressure: {HealthMetrics.blood_pressure ?? "N/A"}</p>
                <p>Blood Glucose: {HealthMetrics.blood_glucose ?? "N/A"}</p>
                <p>Sleep Quality: {HealthMetrics.sleep_quality ?? "N/A"}</p>
                <p>Body Temperature: {HealthMetrics.body_temperature ?? "N/A"}</p>
                <p>Respiratory Rate: {HealthMetrics.respiratory_rate ?? "N/A"}</p>
                <p>
                  Menstrual Cycle: {HealthMetrics.menstrual_cycle_tracker
                  ? JSON.stringify(HealthMetrics.menstrual_cycle_tracker)
                  : "N/A"}
                </p>
                <p>
                  Hydration: {HealthMetrics.hydration
                  ? JSON.stringify(HealthMetrics.hydration)
                  : "N/A"}
                </p>
                <p>
                  Mood: {HealthMetrics.mood_tracker
                  ? JSON.stringify(HealthMetrics.mood_tracker)
                  : "N/A"}
                </p>
                <p>
                  Alerts/Warnings: {HealthMetrics.alert_warnings
                  ? JSON.stringify(HealthMetrics.alert_warnings)
                  : "N/A"}
                </p>
            </div>
        </div>
    )
}
