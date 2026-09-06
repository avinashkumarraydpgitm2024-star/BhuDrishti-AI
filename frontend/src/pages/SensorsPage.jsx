import { useEffect, useState } from "react";

import apiClient from "../api/client";

import "./SensorsPage.css";


function formatLabel(value) {
  if (!value) {
    return "—";
  }

  return String(value).replaceAll("_", " ");
}


function formatTime(value) {
  if (!value) {
    return "—";
  }

  return new Date(value).toLocaleString();
}


function TelemetryItem({ label, value, unit }) {
  return (
    <div className="sensor-telemetry-item">
      <span>{label}</span>

      <strong>
        {value ?? "—"}
        {value !== null && value !== undefined && unit
          ? ` ${unit}`
          : ""}
      </strong>
    </div>
  );
}


export default function SensorsPage() {
  const [sensors, setSensors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const loadSensors = async () => {
      try {
        setLoading(true);
        setError("");

        const sensorResponse = await apiClient.get("/sensors");
        const sensorList = sensorResponse.data;

        const sensorsWithReadings = await Promise.all(
          sensorList.map(async (sensor) => {
            try {
              const readingResponse = await apiClient.get(
                `/sensor-readings/${sensor.public_id}/latest`
              );

              return {
                ...sensor,
                latest_reading: readingResponse.data,
              };
            } catch (err) {
              if (err?.response?.status === 404) {
                return {
                  ...sensor,
                  latest_reading: null,
                };
              }

              throw err;
            }
          })
        );

        setSensors(sensorsWithReadings);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load sensor intelligence."
        );
      } finally {
        setLoading(false);
      }
    };

    loadSensors();
  }, []);


  if (loading) {
    return (
      <div className="sensors-state">
        Loading sensor intelligence...
      </div>
    );
  }


  if (error) {
    return (
      <div className="sensors-state sensors-error">
        {error}
      </div>
    );
  }


  return (
    <main className="sensors-page">
      <section className="sensors-header">
        <div>
          <span className="section-kicker">
            IOT SENSOR NETWORK
          </span>

          <h1>Sensors</h1>

          <p>
            Telemetry records from connected field sensors.
          </p>
        </div>

        <div className="sensor-count-card">
          <span>Connected Sensors</span>
          <strong>{sensors.length}</strong>
        </div>
      </section>


      {sensors.length === 0 ? (
        <section className="sensors-empty">
          <h2>No live sensors connected</h2>

          <p>
            BhuDrishti AI is not currently receiving telemetry
            from any registered physical or verified sensor source.
          </p>

          <span>
            STATUS: WAITING FOR REAL SENSOR DATA
          </span>
        </section>
      ) : (
        <section className="sensor-list">
          {sensors.map((sensor) => {
            const reading = sensor.latest_reading;

            return (
              <article
                className="sensor-card"
                key={sensor.public_id}
              >
                <div className="sensor-card-header">
                  <div>
                    <span className="sensor-code">
                      {sensor.sensor_code}
                    </span>

                    <h2>{sensor.name}</h2>

                    <p>
                      {formatLabel(sensor.sensor_type)}
                    </p>
                  </div>

                  <span className="sensor-status">
                    {formatLabel(sensor.status)}
                  </span>
                </div>


                {reading ? (
                  <>
                    <div className="sensor-live-status">
                      Verified live telemetry available
                    </div>

                    <div className="sensor-telemetry-grid">
                      <TelemetryItem
                        label="Soil Moisture"
                        value={reading.soil_moisture_percent}
                        unit="%"
                      />

                      <TelemetryItem
                        label="Rainfall"
                        value={reading.rainfall_mm}
                        unit="mm"
                      />

                      <TelemetryItem
                        label="Rainfall Rate"
                        value={reading.rainfall_rate_mm_hr}
                        unit="mm/hr"
                      />

                      <TelemetryItem
                        label="Temperature"
                        value={reading.temperature_c}
                        unit="°C"
                      />

                      <TelemetryItem
                        label="Humidity"
                        value={reading.humidity_percent}
                        unit="%"
                      />

                      <TelemetryItem
                        label="Battery"
                        value={reading.battery_level_percent}
                        unit="%"
                      />

                      <TelemetryItem
                        label="Signal"
                        value={reading.signal_strength_dbm}
                        unit="dBm"
                      />

                      <TelemetryItem
                        label="Data Quality"
                        value={reading.data_quality_status}
                      />
                    </div>

                    <div className="sensor-reading-meta">
                      <span>
                        Event: {reading.device_event_id}
                      </span>

                      <span>
                        Recorded: {formatTime(reading.recorded_at)}
                      </span>

                      <span>
                        Received: {formatTime(reading.received_at)}
                      </span>
                    </div>
                  </>
                ) : (
                  <div className="sensor-no-reading">
                    No telemetry received from this sensor yet.
                  </div>
                )}
              </article>
            );
          })}
        </section>
      )}
    </main>
  );
}