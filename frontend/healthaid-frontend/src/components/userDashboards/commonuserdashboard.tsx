import { FaUserCircle } from "react-icons/fa";
import '../../styles/userdashboards/commonuserdashboard.css';
import {
    Profile,
    ProfileData,
    HealthMetricsData
} from "../commonUser/userprofile";

function CommonUserDashboard  () {
    return (
        <div className="commonuserdashboard">
            <section className="section1">
                Personal Info
                <aside className="profilepic">
                    <FaUserCircle size={50}/>
                </aside>
                <>
                <Profile
                PersonalInfo={{
                    full_name: "Edafe Merit",
                    email: "",
                    phone_number: "",
                    emergency_contact: {
                        name: "",
                        email: "",
                    }
                }}
                />
                </>
            </section>
            <section className="section2">
                Bio Data
                <>
                <ProfileData
                BioData={{
                    gender: "",
                    age: 0,
                    height: 0,
                    weight: 0,
                    dob: "",
                    bmi: new Float32Array([0]),
                    blood_type: ""
                }}
                />
                </>
            </section>
            <section className="section3">
                Health Metrics
                <>
                <HealthMetricsData
                HealthMetrics={{
                    blood_pressure: 0,
                    heart_rate: 0,
                    blood_glucose: 0,
                    sleep_quality: "",
                    body_temperature: 0
                }}
                />
                </>
            </section>
        </div>
    )
}

export default CommonUserDashboard;