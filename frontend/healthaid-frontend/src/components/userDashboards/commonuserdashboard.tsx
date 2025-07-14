import '../../styles/userdashboards/commonuserdashboard.css';
import { FaUserCircle } from "react-icons/fa";

function CommonUserDashboard  () {
    return (
        <div className="commonuserdashboard">
            <section className="section1">
                Personal Info
                <aside className="profilepic">
                    <FaUserCircle size={30}/>
                </aside>
            </section>
            <section className="section2">
                Bio Data
            </section>
            <section className="section3">
                Health Metrics
            </section>
        </div>
    )
}

export default CommonUserDashboard;