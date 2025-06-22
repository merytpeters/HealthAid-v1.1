import { Outlet } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";
import Sidebar from "./sidebar";
import HealthaidLogo from "../assets/healthaidlogo";
import '../styles/layout.css'

const Layout = () => {
  return (
    <div className="layout-container">
      <header>
        <HealthaidLogo />
        <aside className="profilepic">
          <FaUserCircle size={30}/>
        </aside>
      </header>
      <div className="page-content">
        <Sidebar />
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;

