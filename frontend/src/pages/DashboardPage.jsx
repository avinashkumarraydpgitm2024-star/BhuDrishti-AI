import { useEffect, useMemo, useState } from "react";

import apiClient from "../api/client";
import HazardMap from "../components/map/HazardMap";

import "./DashboardPage.css";


const RISK_ZONE_ID = "fe1f520f-e8a0-40bd-9eb1-c876502a28d1";


export default function DashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await apiClient.get(
          `/gis/map-data/${RISK_ZONE_ID}`
        );

        setDashboard(response.data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load dashboard data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);


  const currentRisk = useMemo(() => {
    return (
      dashboard?.latest_risk_assessment
        ?.risk_probability_percent ?? null
    );
  }, [dashboard]);


  const severity = useMemo(() => {
    return (
      dashboard?.latest_risk_assessment?.severity ||
      "UNKNOWN"
    );
  }, [dashboard]);


  const isTestData = useMemo(() => {
    const zoneCode =
      dashboard?.risk_zone?.zone_code?.toLowerCase() || "";

    const modelName =
      dashboard?.latest_risk_assessment?.model_name?.toLowerCase() || "";

    return (
      zoneCode.startsWith("test") ||
      modelName.startsWith("test")
    );
  }, [dashboard]);


  const isAssessmentExpired = useMemo(() => {
    const validUntil =
      dashboard?.latest_risk_assessment?.valid_until;

    if (!validUntil) {
      return false;
    }

    return new Date(validUntil).getTime() < Date.now();
  }, [dashboard]);


  const intelligenceStatus = useMemo(() => {
    if (isTestData) {
      return "TEST / CONTROLLED DATA";
    }

    if (isAssessmentExpired) {
      return "HISTORICAL / EXPIRED";
    }

    return "LATEST AVAILABLE DATA";
  }, [isTestData, isAssessmentExpired]);


  const satelliteObservation =
    dashboard?.latest_satellite_observation ?? null;


  if (loading) {
    return (
      <div className="dashboard-state">
        <div className="dashboard-loader" />
        <p>Loading BhuDrishti intelligence...</p>
      </div>
    );
  }


  if (error) {
    return (
      <div className="dashboard-state dashboard-error">
        <h2>Dashboard unavailable</h2>
        <p>{error}</p>
      </div>
    );
  }


  return (
    <main className="dashboard-main">
      <section className="zone-banner">
        <div>
          <span className="section-kicker">
            CONFIGURED MONITORING ZONE
          </span>

          <h3>{dashboard.risk_zone.name}</h3>

          <p>
            {dashboard.risk_zone.district},{" "}
            {dashboard.risk_zone.state}
          </p>
        </div>

        <div className="zone-metadata">
          <div>
            <span>Terrain</span>
            <strong>
              {dashboard.risk_zone.terrain_type || "Unknown"}
            </strong>
          </div>

          <div>
            <span>Elevation</span>
            <strong>
              {dashboard.risk_zone.elevation_m ?? "N/A"} m
            </strong>
          </div>

          <div>
            <span>Slope</span>
            <strong>
              {dashboard.risk_zone.slope_degrees ?? "N/A"}ï¿½
            </strong>
          </div>
        </div>
      </section>


      <section className="overview-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">
              RISK INTELLIGENCE
            </span>

            <h3>Risk Overview</h3>
          </div>

          <span className="live-badge">
            <span />
            {intelligenceStatus}
          </span>
        </div>


        <div className="metric-grid">
          <article className="metric-card risk-card">
            <div className="metric-top">
              <span>Latest Risk Assessment</span>
              <span className="metric-code">AI</span>
            </div>

            <strong className="metric-value">
              {currentRisk !== null
                ? `${currentRisk}%`
                : "N/A"}
            </strong>

            <div className="risk-footer">
              <span className="severity-pill">
                {severity}
              </span>

              <span>Recorded hazard probability</span>
            </div>
          </article>


          <article className="metric-card">
            <div className="metric-top">
              <span>Active Alerts</span>
              <span className="metric-code">AL</span>
            </div>

            <strong className="metric-value">
              {dashboard.active_alert_count}
            </strong>

            <p>Unresolved hazard notifications</p>
          </article>


          <article className="metric-card">
            <div className="metric-top">
              <span>Blocked Roads</span>
              <span className="metric-code">RD</span>
            </div>

            <strong className="metric-value">
              {dashboard.blocked_road_count}
            </strong>

            <p>Road segments currently blocked</p>
          </article>


          <article className="metric-card">
            <div className="metric-top">
              <span>Monitored Villages</span>
              <span className="metric-code">VL</span>
            </div>

            <strong className="metric-value">
              {dashboard.village_count}
            </strong>

            <p>Settlements in monitored zone</p>
          </article>
        </div>
      </section>


      <section className="satellite-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">
              SATELLITE INTELLIGENCE
            </span>

            <h3>Sentinel-2 Observation</h3>
          </div>

          <span className="panel-tag">
            SATELLITE
          </span>
        </div>

        <div className="satellite-card">
          <div className="satellite-header">
            <div>
              <strong>
                {satelliteObservation?.satellite_name ||
                  "Sentinel-2"}
              </strong>

              <span>
                {satelliteObservation?.provider ||
                  "Copernicus Data Space"}
              </span>
            </div>

            <span className="satellite-status">
              {satelliteObservation
                ? "OBSERVATION AVAILABLE"
                : "NO OBSERVATION"}
            </span>
          </div>

          <div className="satellite-metrics">
            <div>
              <span>NDVI</span>
              <strong>
                {satelliteObservation?.ndvi != null
                  ? satelliteObservation.ndvi.toFixed(3)
                  : "N/A"}
              </strong>
              <small>Vegetation index</small>
            </div>

            <div>
              <span>NDWI</span>
              <strong>
                {satelliteObservation?.ndwi != null
                  ? satelliteObservation.ndwi.toFixed(3)
                  : "N/A"}
              </strong>
              <small>Water index</small>
            </div>

            <div>
              <span>SOIL MOISTURE</span>
              <strong>
                {satelliteObservation?.soil_moisture_index != null
                  ? satelliteObservation.soil_moisture_index.toFixed(3)
                  : "N/A"}
              </strong>
              <small>Satellite-derived index</small>
            </div>

            <div>
              <span>CLOUD COVER</span>
              <strong>
                {satelliteObservation?.cloud_cover_percent != null
                  ? `${satelliteObservation.cloud_cover_percent.toFixed(1)}%`
                  : "N/A"}
              </strong>
              <small>Scene quality</small>
            </div>
          </div>

          <div className="satellite-meta">
            <div>
              <span>Captured</span>
              <strong>
                {satelliteObservation?.captured_at
                  ? new Date(
                      satelliteObservation.captured_at
                    ).toLocaleString()
                  : "No observation available"}
              </strong>
            </div>

            <div>
              <span>Scene ID</span>
              <strong>
                {satelliteObservation?.scene_id || "N/A"}
              </strong>
            </div>
          </div>
        </div>
      </section>

      <section className="dashboard-grid">
        <article className="panel map-panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">
                GEOSPATIAL INTELLIGENCE
              </span>

              <h3>GIS Hazard Map</h3>
            </div>

            <span className="panel-tag">
              GIS MAP
            </span>
          </div>

          <div className="map-wrapper">
            <HazardMap
              riskZone={dashboard.risk_zone}
              villages={dashboard.villages}
              roadSegments={dashboard.road_segments}
              latestRiskAssessment={
                dashboard.latest_risk_assessment
              }
            />
          </div>

          <div className="map-legend">
            <div>
              <span className="legend-dot danger" />
              Risk zone
            </div>

            <div>
              <span className="legend-dot village" />
              Village
            </div>

            <div>
              <span className="legend-line open" />
              Open road
            </div>

            <div>
              <span className="legend-line blocked" />
              Blocked road
            </div>
          </div>
        </article>


        <aside className="panel alerts-panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">
                EARLY WARNING
              </span>

              <h3>Latest Alerts</h3>
            </div>

            <span className="alert-count">
              {dashboard.active_alert_count}
            </span>
          </div>


          <div className="alerts-list">
            {dashboard.active_alerts.length === 0 ? (
              <div className="empty-alert-state">
                <div className="safe-icon">
                  OK
                </div>

                <strong>No active alerts</strong>

                <p>
                  No unresolved hazard warning is
                  currently active for this zone.
                </p>
              </div>
            ) : (
              dashboard.active_alerts.map((alert) => (
                <article
                  className="alert-item"
                  key={alert.public_id}
                >
                  <div className="alert-item-top">
                    <strong>{alert.title}</strong>
                    <span>{alert.severity}</span>
                  </div>

                  <p>{alert.message}</p>
                </article>
              ))
            )}
          </div>


          <div className="notification-summary">
            <div>
              <span>Delivered</span>
              <strong>
                {dashboard.delivered_notification_count}
              </strong>
            </div>

            <div>
              <span>Failed</span>
              <strong>
                {dashboard.failed_notification_count}
              </strong>
            </div>
          </div>
        </aside>
      </section>
    </main>
  );
}





