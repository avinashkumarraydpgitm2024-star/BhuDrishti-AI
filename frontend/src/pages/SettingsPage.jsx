import { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./SettingsPage.css";

export default function SettingsPage() {
  const navigate = useNavigate();

  const [autoRefresh, setAutoRefresh] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [mapSatellite, setMapSatellite] = useState(true);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    localStorage.setItem(
      "bhudrishti_settings",
      JSON.stringify({
        autoRefresh,
        notifications,
        mapSatellite,
      })
    );

    setSaved(true);

    setTimeout(() => {
      setSaved(false);
    }, 2500);
  };

  return (
    <main className="settings-page">
      <section className="settings-header">
        <div>
          <span className="section-kicker">
            COMMAND CENTER CONFIGURATION
          </span>

          <h1>Settings</h1>

          <p>
            Configure monitoring, notification and visualization
            preferences for the BhuDrishti command center.
          </p>
        </div>

        <div className="settings-system-card">
          <span>SYSTEM</span>
          <strong>ONLINE</strong>
          <small>Configuration service available</small>
        </div>
      </section>

      {saved && (
        <div className="settings-success">
          Settings saved successfully.
        </div>
      )}

      <section className="settings-grid">
        <article className="settings-panel">
          <div className="settings-panel-heading">
            <span className="section-kicker">
              MONITORING
            </span>
            <h2>Monitoring Preferences</h2>
          </div>

          <label className="settings-row">
            <span>
              <strong>Automatic data refresh</strong>
              <small>
                Keep command center information updated automatically.
              </small>
            </span>

            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(event) =>
                setAutoRefresh(event.target.checked)
              }
            />
          </label>

          <label className="settings-row">
            <span>
              <strong>Early warning notifications</strong>
              <small>
                Enable notification handling for new hazard warnings.
              </small>
            </span>

            <input
              type="checkbox"
              checked={notifications}
              onChange={(event) =>
                setNotifications(event.target.checked)
              }
            />
          </label>

          <label className="settings-row">
            <span>
              <strong>Satellite map preference</strong>
              <small>
                Prefer satellite visualization when available.
              </small>
            </span>

            <input
              type="checkbox"
              checked={mapSatellite}
              onChange={(event) =>
                setMapSatellite(event.target.checked)
              }
            />
          </label>
        </article>

        <article className="settings-panel">
          <div className="settings-panel-heading">
            <span className="section-kicker">
              PLATFORM
            </span>
            <h2>System Information</h2>
          </div>

          <div className="settings-info">
            <span>Platform</span>
            <strong>BhuDrishti AI</strong>
          </div>

          <div className="settings-info">
            <span>Environment</span>
            <strong>Development / Prototype</strong>
          </div>

          <div className="settings-info">
            <span>Intelligence</span>
            <strong>Geo-Hazard Risk Engine</strong>
          </div>

          <div className="settings-info">
            <span>Data Sources</span>
            <strong>Sensor + Weather + Satellite</strong>
          </div>
        </article>
      </section>

      <section className="settings-actions">
        <button
          type="button"
          className="settings-save"
          onClick={handleSave}
        >
          Save Configuration
        </button>

        <button
          type="button"
          className="settings-secondary"
          onClick={() => navigate("/dashboard")}
        >
          Back to Command Center
        </button>
      </section>
    </main>
  );
}
