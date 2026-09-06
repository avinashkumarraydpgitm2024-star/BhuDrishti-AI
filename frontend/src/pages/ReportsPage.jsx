import { useEffect, useState } from "react";
import apiClient from "../api/client";
import "./ReportsPage.css";

export default function ReportsPage() {
  const [data, setData] = useState({
    zones: [],
    sensors: [],
    alerts: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadReportData = async () => {
      try {
        setLoading(true);
        setError("");

        const [zonesResponse, sensorsResponse, alertsResponse] =
          await Promise.all([
            apiClient.get("/risk-zones"),
            apiClient.get("/sensors"),
            apiClient.get("/alerts", {
              params: { limit: 100 },
            }),
          ]);

        setData({
          zones: zonesResponse.data || [],
          sensors: sensorsResponse.data || [],
          alerts: alertsResponse.data || [],
        });
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load command center report data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadReportData();
  }, []);

  const activeAlerts = data.alerts.filter(
    (alert) => alert.status === "active"
  ).length;

  const resolvedAlerts = data.alerts.filter(
    (alert) => alert.status === "resolved"
  ).length;

  const activeSensors = data.sensors.filter(
    (sensor) =>
      String(sensor.status || "").toLowerCase() === "active"
  ).length;

  if (loading) {
    return (
      <div className="reports-state">
        Loading intelligence report...
      </div>
    );
  }

  if (error) {
    return (
      <div className="reports-state reports-error">
        {error}
      </div>
    );
  }

  return (
    <main className="reports-page">
      <section className="reports-header">
        <div>
          <span className="section-kicker">
            OPERATIONAL INTELLIGENCE
          </span>

          <h1>Reports</h1>

          <p>
            Consolidated geo-hazard monitoring, sensor and
            early-warning intelligence.
          </p>
        </div>

        <div className="reports-status-card">
          <span>REPORT STATUS</span>
          <strong>LIVE</strong>
          <small>Connected command center data</small>
        </div>
      </section>

      <section className="reports-kpi-grid">
        <article className="reports-kpi">
          <span>Monitoring Zones</span>
          <strong>{data.zones.length}</strong>
          <small>Registered hazard zones</small>
        </article>

        <article className="reports-kpi">
          <span>Active Sensors</span>
          <strong>{activeSensors}</strong>
          <small>Currently operational</small>
        </article>

        <article className="reports-kpi reports-kpi-danger">
          <span>Active Alerts</span>
          <strong>{activeAlerts}</strong>
          <small>Unresolved warnings</small>
        </article>

        <article className="reports-kpi reports-kpi-success">
          <span>Resolved Alerts</span>
          <strong>{resolvedAlerts}</strong>
          <small>Closed warning records</small>
        </article>
      </section>

      <section className="reports-panel">
        <div className="reports-panel-heading">
          <div>
            <span className="section-kicker">
              MONITORING INVENTORY
            </span>
            <h2>Risk Zone Summary</h2>
          </div>
        </div>

        {data.zones.length === 0 ? (
          <div className="reports-empty">
            No monitoring zones are currently registered.
          </div>
        ) : (
          <div className="reports-table-wrap">
            <table className="reports-table">
              <thead>
                <tr>
                  <th>Zone</th>
                  <th>District</th>
                  <th>State</th>
                  <th>Latitude</th>
                  <th>Longitude</th>
                </tr>
              </thead>

              <tbody>
                {data.zones.map((zone) => (
                  <tr key={zone.public_id}>
                    <td>
                      <strong>{zone.name}</strong>
                    </td>
                    <td>{zone.district || "—"}</td>
                    <td>{zone.state || "—"}</td>
                    <td>{zone.latitude ?? "—"}</td>
                    <td>{zone.longitude ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="reports-two-column">
        <article className="reports-panel">
          <div className="reports-panel-heading">
            <div>
              <span className="section-kicker">
                IOT NETWORK
              </span>
              <h2>Sensor Network</h2>
            </div>
          </div>

          <div className="reports-list">
            {data.sensors.length === 0 ? (
              <div className="reports-empty">
                No registered sensors.
              </div>
            ) : (
              data.sensors.map((sensor) => (
                <div
                  className="reports-list-item"
                  key={sensor.public_id}
                >
                  <div>
                    <strong>{sensor.name}</strong>
                    <span>
                      {sensor.sensor_code} ·{" "}
                      {String(sensor.sensor_type || "").replaceAll(
                        "_",
                        " "
                      )}
                    </span>
                  </div>

                  <b
                    className={`report-sensor-status report-status-${String(
                      sensor.status || ""
                    ).toLowerCase()}`}
                  >
                    {sensor.status || "unknown"}
                  </b>
                </div>
              ))
            )}
          </div>
        </article>

        <article className="reports-panel">
          <div className="reports-panel-heading">
            <div>
              <span className="section-kicker">
                EARLY WARNING
              </span>
              <h2>Recent Alerts</h2>
            </div>
          </div>

          <div className="reports-list">
            {data.alerts.length === 0 ? (
              <div className="reports-empty">
                No alert records available.
              </div>
            ) : (
              data.alerts.slice(0, 6).map((alert) => (
                <div
                  className="reports-list-item"
                  key={alert.public_id}
                >
                  <div>
                    <strong>{alert.title}</strong>
                    <span>
                      {alert.severity || "unknown"} ·{" "}
                      {alert.status || "unknown"}
                    </span>
                  </div>

                  <small>
                    {alert.created_at
                      ? new Date(
                          alert.created_at
                        ).toLocaleDateString()
                      : "—"}
                  </small>
                </div>
              ))
            )}
          </div>
        </article>
      </section>
    </main>
  );
}
