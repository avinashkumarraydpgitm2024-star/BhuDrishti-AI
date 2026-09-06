import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";
import { useTheme } from "../../context/ThemeContext";

import "./AppLayout.css";


export default function AppLayout() {
  const { user, logout } = useAuth();

  const {
    theme,
    toggleTheme,
  } = useTheme();


  return (
    <div className="dashboard-shell">

      <aside className="dashboard-sidebar">

        <div className="brand-block">

          <div className="brand-mark">
            BD
          </div>

          <div>
            <h1>BhuDrishti AI</h1>

            <span>
              Geo-Hazard Command Center
            </span>
          </div>

        </div>


        <nav className="sidebar-nav">

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>01</span>
            Overview
          </NavLink>


          <NavLink
            to="/gis"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>02</span>
            GIS Intelligence
          </NavLink>


          <NavLink
            to="/risk"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>03</span>
            Risk Monitoring
          </NavLink>


          <NavLink
            to="/rain"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>04</span>
            Rain Status
          </NavLink>


          <NavLink
            to="/alerts"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>05</span>
            Alerts
          </NavLink>


          <NavLink
            to="/sensors"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>06</span>
            Sensors
          </NavLink>

          <NavLink
            to="/reports"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>07</span>
            Reports
          </NavLink>

          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>08</span>
            Settings
          </NavLink>

        </nav>


        <div className="sidebar-footer">

          <div className="system-status">

            <span className="status-dot" />

            <div>
              <strong>
                System Online
              </strong>

              <small>
                Intelligence services available
              </small>
            </div>

          </div>


          <button
            type="button"
            className="logout-button"
            onClick={logout}
          >
            Logout
          </button>

        </div>

      </aside>


      <div className="dashboard-content">

        <header className="dashboard-topbar">

          <div className="topbar-heading">

            <p className="eyebrow">
              NORTH-EAST INDIA - HAZARD MONITORING
            </p>

            <h2>
              BhuDrishti AI Command Center
            </h2>

            <p className="topbar-description">
              Geo-hazard intelligence and early warning operations.
            </p>

          </div>


          <div className="topbar-actions">

            <button
              type="button"
              className="theme-toggle"
              onClick={toggleTheme}
              aria-label={
                theme === "dark"
                  ? "Switch to light mode"
                  : "Switch to dark mode"
              }
              title={
                theme === "dark"
                  ? "Switch to light mode"
                  : "Switch to dark mode"
              }
            >

              <span className="theme-toggle-icon">
                {theme === "dark"
                  ? "LIGHT"
                  : "DARK"}
              </span>

              <span className="theme-toggle-label">
                {theme === "dark"
                  ? "Light Mode"
                  : "Dark Mode"}
              </span>

            </button>


            <div className="topbar-user">

              <div className="user-avatar">

                {(user?.full_name || user?.email || "U")
                  .charAt(0)
                  .toUpperCase()}

              </div>


              <div>

                <strong>
                  {user?.full_name || user?.email}
                </strong>

                <span>
                  {user?.role || "User"}
                </span>

              </div>

            </div>

          </div>

        </header>


        <Outlet />

      </div>

    </div>
  );
}
