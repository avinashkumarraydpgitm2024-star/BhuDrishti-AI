import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";


export default function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="dashboard-shell">
      <aside className="dashboard-sidebar">
        <div className="brand-block">
          <div className="brand-mark">
            BD
          </div>

          <div>
            <h1>BhuDrishti AI</h1>
            <span>Geo-Hazard Command Center</span>
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
            to="/alerts"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>04</span>
            Alerts
          </NavLink>

          <NavLink
            to="/sensors"
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>05</span>
            Sensors
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <div className="system-status">
            <span className="status-dot" />

            <div>
              <strong>System Online</strong>
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
          <div>
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
        </header>

        <Outlet />
      </div>
    </div>
  );
}



