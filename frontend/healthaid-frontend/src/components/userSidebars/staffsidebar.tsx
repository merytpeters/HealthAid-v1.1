import { Link } from 'react-router-dom';
import '../../styles/usersidebars/allusersidebar.css';
import {
    FaTimes,
    FaTachometerAlt,
    FaUserInjured,
    FaCalendarCheck
} from 'react-icons/fa';

function StaffSideBar ({ onClose }: { onClose: () => void }) {
    return (
        <div className="asidebar">
            <button className="sidebar-close-btn" onClick={onClose}>
                <FaTimes />
            </button>
            <nav>
                <ul>
                    <li><Link to="/app/dashboard"><FaTachometerAlt /> Dashboard</Link></li>
                    <li><Link to="/app/users"><FaUserInjured /> Patient</Link></li>
                    <li><Link to="/app/reports"><FaCalendarCheck /> Appointments</Link></li>
                </ul>
            </nav>
        </div>
    )
}


export default StaffSideBar;