import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { Outlet } from "react-router-dom";
import HealthaidLogo from "../../assets/healthaidlogo";
import '../../styles/layout.css'

const AuthLayout = () => {
  const [isSignup, setIsSignup] = useState(false);

  const location = useLocation();

  React.useEffect(() => {
    setIsSignup(location.pathname.includes("signup"));
  }, [location.pathname]);

  return (
    <div className='auth-layout-container '>
      <header className='logo'>
        <HealthaidLogo textColor="#FFFFFF"/>
      </header>
      <div className="auth-page-content">
        <div className="hero-message">
          Manage <br /> Chronic Conditions <br />With Ease
          </div>
        <main className="auth-main-content">
          <Outlet />
        </main>
      <div className="bottom-tag-text">
        {isSignup ? (<div>Already have an account ? <a href="/login">Login</a></div>) : (
          <div>Need an account ? <a href="/signup">Sign Up</a></div>
        )}
      </div>
      </div>
    </div>
  );
};

export default AuthLayout;
