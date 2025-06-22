import { Link } from "react-router-dom";
import { useState } from "react";
import '../../styles/usersidebars/allusersidebar.css';
import { 
    FaTachometerAlt,
    FaBook,
    FaPills,
    FaBoxes,
    FaStethoscope,
    FaCapsules,
    FaFirstAid,
    FaCog,
    FaBars,
    FaTimes
} from 'react-icons/fa';

function CommonUserSideBar () {
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
                <li><Link to="/app/journal"><FaBook /> Journal</Link></li>
                <li><Link to="/app/meds"><FaPills /> Meds</Link></li>
                <li><Link to="/app/inventory"><FaBoxes /> Inventory</Link></li>
                <li><Link to="/app/symptom-checker"><FaStethoscope /> Symptom Checker</Link></li>
                <li><Link to="/app/drug-checker"><FaCapsules /> Drug Checker</Link></li>
                <li><Link to="/app/first-aid"><FaFirstAid /> First Aid</Link></li>
                <li><Link to="/app/settings"><FaCog /> Settings</Link></li>
              </ul>
              </nav>
        </div>
    )
}

export default CommonUserSideBar;