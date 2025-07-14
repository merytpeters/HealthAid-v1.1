import { Link } from "react-router-dom";
import '../../styles/usersidebars/allusersidebar.css';
import {
    FaTimes,
    FaTachometerAlt,
    FaUsers,
    FaFileAlt 
} from "react-icons/fa";

function OrgSideBar({ onClose }: { onClose: () => void }) {
    return (
        <div className="asidebar">
            <button className="sidebar-close-btn" onClick={onClose}>
                <FaTimes />
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