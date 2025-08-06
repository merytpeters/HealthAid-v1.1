import { Outlet } from "react-router-dom";
import { useState } from "react";
import Sidebar from "./sidebar";
import HealthaidLogo from "../assets/healthaidlogo";
import '../styles/layout.css'

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className={`layout-container ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <header className={sidebarOpen ? "" : "hidden"}>
        <HealthaidLogo textColor="#FFFFFF"/>
      </header>
      <div className="page-content">
        {sidebarOpen && <Sidebar onClose={() => setSidebarOpen(false)} />}
        <main className="main-content">
          {!sidebarOpen && (
            <button
              className="open-sidebar-btn"
              onClick={() => setSidebarOpen(true)}
            >
              ≡
            </button>
          )}
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;

