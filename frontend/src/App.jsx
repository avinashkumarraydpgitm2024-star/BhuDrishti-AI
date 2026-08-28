import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";
import AppLayout from "./components/layout/AppLayout";

import DashboardPage from "./pages/DashboardPage";
import GISIntelligencePage from "./pages/GISIntelligencePage";
import RiskMonitoringPage from "./pages/RiskMonitoringPage";
import AlertsPage from "./pages/AlertsPage";
import SensorsPage from "./pages/SensorsPage";
import LoginPage from "./pages/LoginPage";


export default function App() {
  return (
    <Routes>
      <Route
        path="/login"
        element={<LoginPage />}
      />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route
            path="/dashboard"
            element={<DashboardPage />}
          />

          <Route
            path="/gis"
            element={<GISIntelligencePage />}
          />

          <Route
            path="/risk"
            element={<RiskMonitoringPage />}
          />

          <Route
            path="/alerts"
            element={<AlertsPage />}
          />

          <Route
            path="/sensors"
            element={<SensorsPage />}
          />
        </Route>
      </Route>

      <Route
        path="/"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />

      <Route
        path="*"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />
    </Routes>
  );
}
