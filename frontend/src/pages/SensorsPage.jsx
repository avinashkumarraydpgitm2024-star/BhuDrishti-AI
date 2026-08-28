import { useEffect, useState } from "react";

import apiClient from "../api/client";

import "./SensorsPage.css";


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
          {sensors.map((sensor) => (
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

                  <p>{sensor.sensor_type}</p>
                </div>

                <span className="sensor-status">
                  {sensor.status}
                </span>
              </div>

              {sensor.latest_reading ? (
                <div className="sensor-live-status">
                  Verified live reading available
                </div>
              ) : (
                <div className="sensor-no-reading">
                  No telemetry received from this sensor yet.
                </div>
              )}
            </article>
          ))}
        </section>
      )}
    </main>
  );
}


