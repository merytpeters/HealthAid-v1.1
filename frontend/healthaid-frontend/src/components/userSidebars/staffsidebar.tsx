import { useState } from 'react';
import { Link } from 'react-router-dom';
import '../../styles/usersidebars/allusersidebar.css';
import {
    FaTimes,
    FaBars,
    FaTachometerAlt,
    FaUserInjured,
    FaCalendarCheck
} from 'react-icons/fa';

function StaffSideBar () {
    const [isOpen, setIsOpen] = useState(true);

    const toggleSidebar = () => setIsOpen(!isOpen);
    return (
        <div className={`asidebar ${isOpen ? "" : "closed"}`}>
            <button
                className="toggle-button"
                onClick={toggleSidebar}
                aria-label={isOpen ? "Collapse sidebar" : "Expand sidebar"}
            >
            {isOpen ? <FaTimes size={20} /> : <FaBars size={15} />}
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