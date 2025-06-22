import { useState } from "react";
import { Link } from "react-router-dom";
import '../../styles/usersidebars/allusersidebar.css';
import {
    FaTimes,
    FaBars,
    FaTachometerAlt,
    FaUsers,
    FaFileAlt 
} from "react-icons/fa";

function OrgSideBar() {
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
                    <li><Link to="/app/users"><FaUsers /> Users</Link></li>
                    <li><Link to="/app/reports"><FaFileAlt /> Reports</Link></li>
                </ul>
            </nav>
        </div>
    )
}

export default OrgSideBar;