import { useEffect, useMemo, useState } from "react";

import apiClient from "../api/client";
import HazardMap from "../components/map/HazardMap";

import "./DashboardPage.css";

const RISK_ZONE_ID = "fe1f520f-e8a0-40bd-9eb1-c876502a28d1";

function formatNumber(value, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "N/A";
  }
  return Number(value).toFixed(digits);
}

function formatTime(value) {
  if (!value) return "N/A";
  return new Date(value).toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function riskTone(severity) {
  const value = String(severity || "").toLowerCase();
  if (value === "critical") return "critical";
  if (value === "high") return "high";
  if (value === "moderate" || value === "medium") return "moderate";
  return "low";
}

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [sensors, setSensors] = useState([]);
  const [riskHistory, setRiskHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        setError("");

        const [dashboardResponse, sensorResponse, historyResponse] =
          await Promise.all([
            apiClient.get(`/gis/map-data/${RISK_ZONE_ID}`),
            apiClient.get("/sensors"),
            apiClient.get(`/risk-assessments/history/${RISK_ZONE_ID}`),
          ]);

        const sensorList = sensorResponse.data || [];
        let sensorWithReading = null;

        if (sensorList.length > 0) {
          const sensor = sensorList[0];

          try {
            const readingResponse = await apiClient.get(
              `/sensor-readings/${sensor.public_id}/latest`
            );

            sensorWithReading = {
              ...sensor,
              latest_reading: readingResponse.data,
            };
          } catch (readingError) {
            if (readingError?.response?.status === 404) {
              sensorWithReading = {
                ...sensor,
                latest_reading: null,
              };
            } else {
              throw readingError;
            }
          }
        }

        const historyPayload = historyResponse.data;
        const historyList = Array.isArray(historyPayload)
          ? historyPayload
          : historyPayload?.items ||
            historyPayload?.assessments ||
            historyPayload?.data ||
            [];

        setDashboard({
          ...dashboardResponse.data,
          sensor: sensorWithReading,
        });
        setSensors(sensorList);
        setRiskHistory(historyList);
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

  const risk = dashboard?.latest_risk_assessment || null;
  const weather = dashboard?.current_weather || null;
  const satellite = dashboard?.latest_satellite_observation || null;
  const forecasts = dashboard?.weather_forecasts || [];
  const sensor = dashboard?.sensor || null;
  const sensorReading = sensor?.latest_reading || null;
  const alerts = dashboard?.active_alerts || [];

  const riskValue = risk?.risk_probability_percent ?? null;
  const severity = risk?.severity || "UNKNOWN";
  const tone = riskTone(severity);

  const activeSensorCount = sensors.filter(
    (item) => String(item?.status || "").toLowerCase() === "active"
  ).length;

  const sensorStatus = useMemo(() => {
    const result = {
      total: sensors.length,
      active: 0,
      maintenance: 0,
      offline: 0,
      faulty: 0,
    };

    sensors.forEach((item) => {
      const status = String(item?.status || "").toLowerCase();
      if (status === "active") result.active += 1;
      else if (status === "maintenance") result.maintenance += 1;
      else if (status === "offline") result.offline += 1;
      else if (status === "faulty") result.faulty += 1;
    });

    return result;
  }, [sensors]);

  const rainfallForecastTotal = useMemo(
    () =>
      forecasts.slice(0, 24).reduce(
        (sum, item) =>
          sum +
          Number(item?.rain_mm ?? item?.precipitation_mm ?? 0),
        0
      ),
    [forecasts]
  );

  const maxForecastRain = useMemo(
    () =>
      Math.max(
        1,
        ...forecasts.slice(0, 24).map((item) =>
          Number(item?.rain_mm ?? item?.precipitation_mm ?? 0)
        )
      ),
    [forecasts]
  );

  const trendPoints = useMemo(() => {
    const source = [...riskHistory]
      .filter((item) => item?.risk_probability_percent != null)
      .sort(
        (a, b) =>
          new Date(a.assessed_at || a.created_at || 0).getTime() -
          new Date(b.assessed_at || b.created_at || 0).getTime()
      )
      .slice(-7);

    if (source.length === 0 && riskValue != null) {
      return [{ label: "Now", value: Number(riskValue) }];
    }

    return source.map((item) => ({
      label: new Date(
        item.assessed_at || item.created_at
      ).toLocaleDateString([], {
        month: "short",
        day: "2-digit",
      }),
      value: Number(item.risk_probability_percent),
    }));
  }, [riskHistory, riskValue]);

  const trendPath = useMemo(() => {
    if (trendPoints.length < 2) return "";

    const left = 20;
    const right = 680;
    const top = 18;
    const bottom = 172;
    const maxIndex = trendPoints.length - 1;

    return trendPoints
      .map((point, index) => {
        const x = left + (index / maxIndex) * (right - left);
        const value = Math.min(100, Math.max(0, point.value));
        const y = bottom - (value / 100) * (bottom - top);
        return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
      })
      .join(" ");
  }, [trendPoints]);

  const intelligenceStatus =
    dashboard?.risk_zone?.zone_code?.toLowerCase().startsWith("test")
      ? "TEST / CONTROLLED DATA"
      : "LIVE INTELLIGENCE";

  if (loading) {
    return (
      <div className="dashboard-state">
        <div className="dashboard-loader" />
        <p>Loading BhuDrishti Intelligence...</p>
      </div>
    );
  }

  if (error || !dashboard) {
    return (
      <div className="dashboard-state dashboard-error">
        <h2>Dashboard unavailable</h2>
        <p>{error || "Dashboard data is unavailable."}</p>
      </div>
    );
  }

  return (
    <main className="dashboard-main reference-dashboard">
      <section className="reference-welcome">
        <div>
          <h1>Welcome to BhuDrishti AI</h1>
          <p>
            Real-time monitoring  AI-powered risk assessment  Early
            warnings  Safer North-East India
          </p>
        </div>

        <button type="button" className="zone-selector">
          <span className="zone-selector-icon"></span>
          <span>{dashboard?.risk_zone?.name || "Monitoring Zone"}</span>
          <span className="zone-selector-arrow"></span>
        </button>
      </section>

      <section className="reference-kpi-grid">
        <article className="reference-kpi monitoring-kpi">
          <div className="kpi-icon"></div>
          <div className="kpi-content">
            <span>Monitoring Zones</span>
            <strong>1</strong>
            <small className="kpi-positive"> 0 this week</small>
          </div>
          <span className="kpi-action"></span>
        </article>

        <article className="reference-kpi sensor-kpi">
          <div className="kpi-icon"></div>
          <div className="kpi-content">
            <span>Active Sensors</span>
            <strong>{activeSensorCount}</strong>
            <small className="kpi-positive">
               {activeSensorCount > 0 ? 1 : 0} this week
            </small>
          </div>
          <span className="kpi-action"></span>
        </article>

        <article className="reference-kpi alert-kpi">
          <div className="kpi-icon">!</div>
          <div className="kpi-content">
            <span>Active Alerts</span>
            <strong>{dashboard.active_alert_count ?? 0}</strong>
            <small className="kpi-positive">
               {dashboard.active_alert_count ?? 0} this week
            </small>
          </div>
          <span className="kpi-action"></span>
        </article>

        <article className={`reference-kpi risk-kpi ${tone}`}>
          <div className="kpi-icon"></div>
          <div className="kpi-content">
            <span>Avg. Risk Level</span>
            <strong>
              {riskValue !== null ? `${formatNumber(riskValue)}%` : "N/A"}
            </strong>
            <small className={tone === "low" ? "kpi-positive" : "kpi-warning"}>
              {String(severity).toLowerCase()}
            </small>
          </div>
          <span className="kpi-action"></span>
        </article>
      </section>

      <section className="reference-primary-grid">
        <article className="reference-panel reference-map-panel">
          <div className="reference-panel-header">
            <div>
              <span>RISK ZONES MAP</span>
              <h2>Real-time hazard risk levels across monitoring zones</h2>
            </div>
            <button type="button" className="map-view-button">
              Satellite View
            </button>
          </div>

          <div className="reference-map">
            <HazardMap
              riskZone={dashboard?.risk_zone}
              villages={dashboard?.villages || []}
              roadSegments={dashboard?.road_segments || []}
              latestRiskAssessment={dashboard?.latest_risk_assessment}
            />
          </div>

          <div className="reference-map-legend">
            <span><i className="legend-dot low" />Low</span>
            <span><i className="legend-dot moderate" />Moderate</span>
            <span><i className="legend-dot high" />High</span>
            <span><i className="legend-dot critical" />Critical</span>
          </div>
        </article>

        <article className="reference-panel reference-alert-panel">
          <div className="reference-panel-header">
            <div>
              <span>RECENT ALERTS</span>
              <h2>Latest notifications and warnings</h2>
            </div>
            <button type="button" className="panel-view-button">View All</button>
          </div>

          <div className="reference-alert-list">
            {alerts.length === 0 ? (
              <div className="reference-no-alerts">
                <div className="no-alert-icon"></div>
                <strong>No active alerts</strong>
                <span>No unresolved hazard warning is currently active.</span>
              </div>
            ) : (
              alerts.slice(0, 5).map((alert) => (
                <div className="reference-alert-item" key={alert.public_id}>
                  <span className={`alert-dot ${String(alert.severity || "").toLowerCase()}`} />
                  <div className="alert-item-content">
                    <strong>{alert.title}</strong>
                    <span>{formatTime(alert.created_at)}</span>
                  </div>
                  <span className={`alert-badge ${String(alert.severity || "").toLowerCase()}`}>
                    {String(alert.severity || "INFO").replace(/_/g, " ")}
                  </span>
                </div>
              ))
            )}
          </div>

          <div className="notification-summary">
            <div>
              <span>Delivered</span>
              <strong>{dashboard.delivered_notification_count ?? 0}</strong>
            </div>
            <div>
              <span>Failed</span>
              <strong>{dashboard.failed_notification_count ?? 0}</strong>
            </div>
          </div>
        </article>

        <article className="reference-panel reference-weather-panel">
          <div className="reference-panel-header">
            <div>
              <span>LIVE WEATHER</span>
              <h2> From Open-Meteo</h2>
            </div>
          </div>

          <div className="weather-location">
            <strong>{dashboard?.risk_zone?.name || "Monitoring Zone"}</strong>
            <span>
              {dashboard?.risk_zone?.latitude ?? "N/A"} N,{" "}
              {dashboard?.risk_zone?.longitude ?? "N/A"} E
            </span>
          </div>

          <div className="weather-temperature">
            <strong>
              {weather?.temperature_c != null
                ? `${weather.temperature_c}C`
                : "N/A"}
            </strong>
            <span>{weather?.weather_description || "Current conditions"}</span>
          </div>

          <div className="weather-stats">
            <div><strong>{weather?.humidity_percent != null ? `${weather.humidity_percent}%` : "N/A"}</strong><span>Humidity</span></div>
            <div><strong>{weather?.rainfall_mm != null ? `${weather.rainfall_mm} mm` : "N/A"}</strong><span>Rainfall</span></div>
            <div><strong>{weather?.wind_speed_mps != null ? `${weather.wind_speed_mps} m/s` : "N/A"}</strong><span>Wind Speed</span></div>
            <div><strong>{weather?.atmospheric_pressure_hpa != null ? `${weather.atmospheric_pressure_hpa} hPa` : "N/A"}</strong><span>Pressure</span></div>
          </div>

          <small className="weather-updated">
            Last updated: {formatTime(weather?.observed_at)}
          </small>
        </article>
      </section>

      <section className="reference-analytics-grid">
        <article className="reference-panel trend-panel">
          <div className="reference-panel-header">
            <div>
              <span>RISK LEVEL TREND</span>
              <h2>Model predicted risk probability</h2>
            </div>
            <div className="current-risk-box">
              <strong>{riskValue !== null ? `${formatNumber(riskValue)}%` : "N/A"}</strong>
              <span>Current Risk</span>
            </div>
          </div>

          <div className="risk-chart">
            <div className="risk-y-axis">
              <span>100%</span><span>75%</span><span>50%</span><span>25%</span><span>0%</span>
            </div>
            <svg viewBox="0 0 700 190" preserveAspectRatio="none" className="risk-svg">
              {[18, 56, 95, 133, 172].map((y) => (
                <line key={y} x1="20" y1={y} x2="680" y2={y} className="chart-grid-line" />
              ))}
              {trendPath && <path d={trendPath} className="risk-line" />}
              {trendPoints.map((point, index) => {
                const x = trendPoints.length === 1
                  ? 350
                  : 20 + (index / Math.max(1, trendPoints.length - 1)) * 660;
                const y = 172 - (Math.min(100, Math.max(0, point.value)) / 100) * 154;
                return <circle key={`${point.label}-${index}`} cx={x} cy={y} r="4.5" className="risk-point" />;
              })}
            </svg>
            <div className="risk-x-axis">
              {trendPoints.map((point, index) => (
                <span key={`${point.label}-${index}`}>{point.label}</span>
              ))}
            </div>
          </div>
        </article>

        <article className="reference-panel rainfall-panel">
          <div className="reference-panel-header">
            <div>
              <span>RAINFALL (24 HOURS)</span>
              <h2>Observed vs forecasted precipitation</h2>
            </div>
            <div className="chart-legend">
              <span><i className="observed-dot" />Observed</span>
              <span><i className="forecast-dot" />Forecast</span>
            </div>
          </div>

          <div className="rainfall-chart">
            <div className="rainfall-bars">
              {forecasts.slice(0, 24).map((forecast) => {
                const rain = Number(forecast?.rain_mm ?? forecast?.precipitation_mm ?? 0);
                const height = Math.max(4, (rain / maxForecastRain) * 100);
                return (
                  <div className="rainfall-column" key={forecast.public_id}>
                    <div className="rainfall-track">
                      <div className="rainfall-bar" style={{ height: `${height}%` }} />
                    </div>
                    <span>
                      {new Date(forecast.forecast_for).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="rainfall-total">
            24H EXPECTED RAIN <strong>{rainfallForecastTotal.toFixed(1)} mm</strong>
          </div>
        </article>

        <article className="reference-panel sensor-status-panel">
          <div className="reference-panel-header">
            <div>
              <span>SENSOR STATUS</span>
              <h2>Real-time sensor network health</h2>
            </div>
            <button type="button" className="panel-view-button">View All</button>
          </div>

          <div className="sensor-status-content">
            <div
              className="sensor-donut"
              style={{
                "--sensor-progress": sensorStatus.total > 0
                  ? `${Math.round((sensorStatus.active / sensorStatus.total) * 100)}%`
                  : "0%",
              }}
            >
              <div>
                <strong>{sensorStatus.total}</strong>
                <span>Total<br />Sensors</span>
              </div>
            </div>

            <div className="sensor-status-legend">
              <div><i className="sensor-status-active" /><span>Active</span><strong>{sensorStatus.active}</strong></div>
              <div><i className="sensor-status-maintenance" /><span>Maintenance</span><strong>{sensorStatus.maintenance}</strong></div>
              <div><i className="sensor-status-offline" /><span>Offline</span><strong>{sensorStatus.offline}</strong></div>
              <div><i className="sensor-status-faulty" /><span>Faulty</span><strong>{sensorStatus.faulty}</strong></div>
            </div>
          </div>
        </article>
      </section>

      <section className="reference-intelligence-strip">
        <article>
          <span>SATELLITE INTELLIGENCE</span>
          <strong>{satellite?.satellite_name || "Sentinel-2"}</strong>
          <small>
            NDVI {satellite?.ndvi != null ? satellite.ndvi.toFixed(3) : "N/A"}
            {"  "}
            NDWI {satellite?.ndwi != null ? satellite.ndwi.toFixed(3) : "N/A"}
            {"  "}
            Soil Index {satellite?.soil_moisture_index != null ? satellite.soil_moisture_index.toFixed(3) : "N/A"}
          </small>
        </article>
        <article>
          <span>LIVE SENSOR TELEMETRY</span>
          <strong>{sensor?.name || "No sensor"}</strong>
          <small>
            Soil Moisture {sensorReading?.soil_moisture_percent ?? "N/A"}%
            {"  "}
            Rain Rate {sensorReading?.rainfall_rate_mm_hr ?? "N/A"} mm/hr
          </small>
        </article>
      </section>

      <div className="reference-data-status">
        <span className="status-pulse" />
        {intelligenceStatus}
        <span>BhuDrishti AI intelligence services</span>
      </div>
    </main>
  );
}


