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

        const [dashboardResponse, sensorResponse] =
          await Promise.all([
            apiClient.get(`/gis/map-data/${RISK_ZONE_ID}`),
            apiClient.get("/sensors"),
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

        setDashboard({
          ...dashboardResponse.data,
          sensor: sensorWithReading,
        });
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
  const satellite =
    dashboard?.latest_satellite_observation || null;
  const forecasts = dashboard?.weather_forecasts || [];
  const sensor = dashboard?.sensor || null;
  const alerts = dashboard?.active_alerts || [];

  const riskValue = risk?.risk_probability_percent ?? null;

  const severity = useMemo(
    () => risk?.severity || "UNKNOWN",
    [risk]
  );

  const severityClass = String(severity)
    .toLowerCase()
    .replace(/_/g, "-");

  const isTestData = useMemo(() => {
    const zoneCode =
      dashboard?.risk_zone?.zone_code?.toLowerCase() || "";

    return zoneCode.startsWith("test");
  }, [dashboard]);

  const isExpired = useMemo(() => {
    if (!risk?.valid_until) return false;
    return new Date(risk.valid_until).getTime() < Date.now();
  }, [risk]);

  const intelligenceStatus = isTestData
    ? "CONTROLLED DATA"
    : isExpired
      ? "HISTORICAL"
      : "LIVE INTELLIGENCE";

  const rainfallForecastTotal = useMemo(
    () =>
      forecasts
        .slice(0, 24)
        .reduce(
          (sum, item) =>
            sum + Number(item?.rain_mm || item?.precipitation_mm || 0),
          0
        ),
    [forecasts]
  );

  const maxForecastRain = useMemo(
    () =>
      Math.max(
        1,
        ...forecasts
          .slice(0, 24)
          .map((item) =>
            Number(item?.rain_mm || item?.precipitation_mm || 0)
          )
      ),
    [forecasts]
  );

  const sensorReading = sensor?.latest_reading || null;

  if (loading) {
    return (
      <div className="dashboard-state">
        <div className="dashboard-loader" />
        <p>Loading BhuDrishti Intelligence Center...</p>
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
    <main className="dashboard-main command-dashboard">

      {/* HEADER */}
      <section className="command-header">
        <div>
          <div className="command-eyebrow">
            BHUDRISHTI AI · GEO-HAZARD INTELLIGENCE
          </div>

          <h1>Risk Intelligence Command Center</h1>

          <p>
            Real-time monitoring of terrain, rainfall, satellite
            observations, IoT telemetry and early-warning signals.
          </p>
        </div>

        <div className="command-header-right">
          <div className="system-live">
            <span className="live-dot" />
            SYSTEM ONLINE
          </div>

          <div className="command-time">
            {new Date().toLocaleString()}
          </div>
        </div>
      </section>

      {/* ZONE BAR */}
      <section className="monitoring-bar">
        <div className="monitoring-location">
          <span className="mini-label">MONITORING ZONE</span>
          <strong>
            {dashboard.risk_zone.name}
          </strong>
          <span>
            {dashboard.risk_zone.district},{" "}
            {dashboard.risk_zone.state}
          </span>
        </div>

        <div className="monitoring-meta">
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
              {dashboard.risk_zone.slope_degrees ?? "N/A"}°
            </strong>
          </div>

          <div>
            <span>Data State</span>
            <strong>{intelligenceStatus}</strong>
          </div>
        </div>
      </section>

      {/* TOP METRICS */}
      <section className="command-metrics">

        <article className={`command-metric risk-metric ${severityClass}`}>
          <div className="metric-heading">
            <span>GEO-HAZARD RISK</span>
            <span className="metric-symbol">AI</span>
          </div>

          <div className="risk-number">
            {riskValue !== null ? `${riskValue}%` : "N/A"}
          </div>

          <div className="risk-meter">
            <span
              style={{
                width: `${Math.min(
                  100,
                  Math.max(0, Number(riskValue || 0))
                )}%`,
              }}
            />
          </div>

          <div className="metric-bottom">
            <strong>{severity}</strong>
            <span>
              Confidence {risk?.confidence_percent ?? "N/A"}%
            </span>
          </div>
        </article>

        <article className="command-metric">
          <div className="metric-heading">
            <span>ACTIVE ALERTS</span>
            <span className="metric-symbol alert-symbol">!</span>
          </div>

          <div className="command-number">
            {dashboard.active_alert_count ?? 0}
          </div>

          <div className="metric-caption">
            Unresolved early-warning notifications
          </div>
        </article>

        <article className="command-metric">
          <div className="metric-heading">
            <span>BLOCKED ROADS</span>
            <span className="metric-symbol">RD</span>
          </div>

          <div className="command-number">
            {dashboard.blocked_road_count ?? 0}
          </div>

          <div className="metric-caption">
            Currently affected road segments
          </div>
        </article>

        <article className="command-metric">
          <div className="metric-heading">
            <span>MONITORED VILLAGES</span>
            <span className="metric-symbol">VL</span>
          </div>

          <div className="command-number">
            {dashboard.village_count ?? 0}
          </div>

          <div className="metric-caption">
            Settlements inside monitoring zone
          </div>
        </article>

      </section>

      {/* MAIN COMMAND GRID */}
      <section className="command-grid">

        {/* MAP */}
        <article className="command-panel map-command-panel">
          <div className="command-panel-header">
            <div>
              <span className="panel-eyebrow">
                GEOSPATIAL INTELLIGENCE
              </span>
              <h2>Hazard Monitoring Map</h2>
            </div>

            <span className="panel-live-tag">
              LIVE GIS
            </span>
          </div>

          <div className="command-map">
            <HazardMap
              riskZone={dashboard.risk_zone}
              villages={dashboard.villages}
              roadSegments={dashboard.road_segments}
              latestRiskAssessment={
                dashboard.latest_risk_assessment
              }
            />
          </div>

          <div className="command-map-footer">
            <span>
              <i className="legend-risk" />
              Risk zone
            </span>

            <span>
              <i className="legend-village" />
              Village
            </span>

            <span>
              <i className="legend-road" />
              Open road
            </span>

            <span>
              <i className="legend-blocked" />
              Blocked road
            </span>
          </div>
        </article>

        {/* ALERTS */}
        <aside className="command-panel alerts-command-panel">
          <div className="command-panel-header">
            <div>
              <span className="panel-eyebrow">
                EARLY WARNING SYSTEM
              </span>
              <h2>Recent Alerts</h2>
            </div>

            <span className="alert-total">
              {dashboard.active_alert_count ?? 0}
            </span>
          </div>

          <div className="command-alerts">
            {alerts.length === 0 ? (
              <div className="command-safe-state">
                <div className="safe-check">✓</div>
                <strong>No active alerts</strong>
                <p>
                  No unresolved hazard notification is currently
                  associated with this monitoring zone.
                </p>
              </div>
            ) : (
              alerts.slice(0, 5).map((alert) => (
                <div
                  className="command-alert"
                  key={alert.public_id}
                >
                  <div className="alert-severity">
                    {alert.severity}
                  </div>

                  <strong>{alert.title}</strong>

                  <p>{alert.message}</p>

                  <small>
                    {alert.created_at
                      ? new Date(
                          alert.created_at
                        ).toLocaleString()
                      : "Time unavailable"}
                  </small>
                </div>
              ))
            )}
          </div>

          <div className="alert-summary">
            <div>
              <span>Delivered</span>
              <strong>
                {dashboard.delivered_notification_count ?? 0}
              </strong>
            </div>

            <div>
              <span>Failed</span>
              <strong>
                {dashboard.failed_notification_count ?? 0}
              </strong>
            </div>
          </div>
        </aside>

      </section>

      {/* INTELLIGENCE ROW */}
      <section className="intelligence-grid">

        {/* WEATHER */}
        <article className="command-panel intelligence-panel">
          <div className="command-panel-header">
            <div>
              <span className="panel-eyebrow">
                ATMOSPHERIC TELEMETRY
              </span>
              <h2>Live Weather</h2>
            </div>

            <span className="source-tag">
              {weather?.provider || "OPEN-METEO"}
            </span>
          </div>

          <div className="weather-command-grid">
            <div className="weather-primary">
              <span>Temperature</span>
              <strong>
                {weather?.temperature_c != null
                  ? `${weather.temperature_c}°C`
                  : "N/A"}
              </strong>
            </div>

            <div>
              <span>Humidity</span>
              <strong>
                {weather?.humidity_percent != null
                  ? `${weather.humidity_percent}%`
                  : "N/A"}
              </strong>
            </div>

            <div>
              <span>Rainfall</span>
              <strong>
                {weather?.rainfall_mm != null
                  ? `${weather.rainfall_mm} mm`
                  : "N/A"}
              </strong>
            </div>

            <div>
              <span>Rain Rate</span>
              <strong>
                {weather?.rainfall_rate_mm_hr != null
                  ? `${weather.rainfall_rate_mm_hr} mm/hr`
                  : "N/A"}
              </strong>
            </div>

            <div>
              <span>Wind</span>
              <strong>
                {weather?.wind_speed_mps != null
                  ? `${weather.wind_speed_mps} m/s`
                  : "N/A"}
              </strong>
            </div>

            <div>
              <span>Pressure</span>
              <strong>
                {weather?.atmospheric_pressure_hpa != null
                  ? `${weather.atmospheric_pressure_hpa}`
                  : "N/A"}
              </strong>
            </div>
          </div>
        </article>

        {/* SENSOR */}
        <article className="command-panel intelligence-panel">
          <div className="command-panel-header">
            <div>
              <span className="panel-eyebrow">
                IoT TELEMETRY
              </span>
              <h2>Sensor Status</h2>
            </div>

            <span className="sensor-online-tag">
              {sensor?.status || "NO SENSOR"}
            </span>
          </div>

          {sensor && sensorReading ? (
            <>
              <div className="sensor-primary">
                <div>
                  <span>{sensor.sensor_code}</span>
                  <strong>{sensor.name}</strong>
                </div>

                <div className="sensor-pulse">
                  <i />
                  LIVE
                </div>
              </div>

              <div className="sensor-command-grid">
                <div>
                  <span>Soil Moisture</span>
                  <strong>
                    {sensorReading.soil_moisture_percent ?? "N/A"}%
                  </strong>
                </div>

                <div>
                  <span>Rainfall</span>
                  <strong>
                    {sensorReading.rainfall_mm ?? "N/A"} mm
                  </strong>
                </div>

                <div>
                  <span>Temperature</span>
                  <strong>
                    {sensorReading.temperature_c ?? "N/A"}°C
                  </strong>
                </div>

                <div>
                  <span>Humidity</span>
                  <strong>
                    {sensorReading.humidity_percent ?? "N/A"}%
                  </strong>
                </div>
              </div>

              <div className="sensor-health">
                <span>
                  Battery{" "}
                  {sensorReading.battery_level_percent ?? "N/A"}%
                </span>

                <span>
                  Signal{" "}
                  {sensorReading.signal_strength_dbm ?? "N/A"} dBm
                </span>

                <span>
                  Quality{" "}
                  {sensorReading.data_quality_status || "N/A"}
                </span>
              </div>
            </>
          ) : (
            <div className="command-empty">
              No live sensor telemetry available.
            </div>
          )}
        </article>

        {/* SATELLITE */}
        <article className="command-panel intelligence-panel">
          <div className="command-panel-header">
            <div>
              <span className="panel-eyebrow">
                EARTH OBSERVATION
              </span>
              <h2>Satellite Intelligence</h2>
            </div>

            <span className="source-tag">
              {satellite?.satellite_name || "SENTINEL-2"}
            </span>
          </div>

          {satellite ? (
            <>
              <div className="satellite-scene">
                <div>
                  <span>SCENE</span>
                  <strong>
                    {satellite.scene_id || "N/A"}
                  </strong>
                </div>

                <div>
                  <span>CLOUD</span>
                  <strong>
                    {satellite.cloud_cover_percent != null
                      ? `${satellite.cloud_cover_percent}%`
                      : "N/A"}
                  </strong>
                </div>
              </div>

              <div className="satellite-command-grid">
                <div>
                  <span>NDVI</span>
                  <strong>
                    {satellite.ndvi != null
                      ? satellite.ndvi.toFixed(3)
                      : "N/A"}
                  </strong>
                </div>

                <div>
                  <span>NDWI</span>
                  <strong>
                    {satellite.ndwi != null
                      ? satellite.ndwi.toFixed(3)
                      : "N/A"}
                  </strong>
                </div>

                <div>
                  <span>Soil Index</span>
                  <strong>
                    {satellite.soil_moisture_index != null
                      ? satellite.soil_moisture_index.toFixed(3)
                      : "N/A"}
                  </strong>
                </div>

                <div>
                  <span>Surface Temp</span>
                  <strong>
                    {satellite.surface_temperature_c != null
                      ? `${satellite.surface_temperature_c}°C`
                      : "N/A"}
                  </strong>
                </div>
              </div>
            </>
          ) : (
            <div className="command-empty">
              No satellite observation available.
            </div>
          )}
        </article>

      </section>

      {/* FORECAST */}
      <section className="command-panel forecast-command-panel">
        <div className="command-panel-header">
          <div>
            <span className="panel-eyebrow">
              PREDICTIVE WEATHER INTELLIGENCE
            </span>
            <h2>24-Hour Rainfall Forecast</h2>
          </div>

          <div className="forecast-total">
            <span>24H EXPECTED RAIN</span>
            <strong>
              {rainfallForecastTotal.toFixed(1)} mm
            </strong>
          </div>
        </div>

        {forecasts.length > 0 ? (
          <div className="forecast-command-chart">
            {forecasts.slice(0, 24).map((forecast) => {
              const rain = Number(
                forecast?.rain_mm ||
                  forecast?.precipitation_mm ||
                  0
              );

              const height = Math.max(
                6,
                (rain / maxForecastRain) * 100
              );

              return (
                <div
                  className="forecast-column"
                  key={forecast.public_id}
                >
                  <div className="forecast-bar-track">
                    <div
                      className="forecast-bar"
                      style={{ height: `${height}%` }}
                    />
                  </div>

                  <strong>
                    {rain.toFixed(1)}
                  </strong>

                  <span>
                    {new Date(
                      forecast.forecast_for
                    ).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="command-empty">
            No forecast records available.
          </div>
        )}
      </section>

      {/* RISK EXPLANATION */}
      <section className="risk-explanation">
        <div>
          <span className="panel-eyebrow">
            AI RISK ASSESSMENT
          </span>

          <h2>
            {risk?.explanation ||
              "Risk assessment explanation is currently unavailable."}
          </h2>
        </div>

        <div className="risk-explanation-meta">
          <div>
            <span>Dominant Factor</span>
            <strong>
              {risk?.dominant_factor || "N/A"}
            </strong>
          </div>

          <div>
            <span>Forecast Horizon</span>
            <strong>
              {risk?.forecast_horizon_minutes
                ? `${risk.forecast_horizon_minutes} min`
                : "N/A"}
            </strong>
          </div>

          <div>
            <span>Model</span>
            <strong>
              {risk?.model_name || "N/A"}
            </strong>
          </div>
        </div>
      </section>

    </main>
  );
}
