import { useEffect, useMemo, useState } from "react";

import apiClient from "../api/client";

import "./RiskMonitoringPage.css";

const RISK_ZONE_ID = "fe1f520f-e8a0-40bd-9eb1-c876502a28d1";

export default function RiskMonitoringPage() {
  const [riskData, setRiskData] = useState(null);
  const [sensorData, setSensorData] = useState(null);
  const [assessmentHistory, setAssessmentHistory] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [generating, setGenerating] = useState(false);
  const [generateMessage, setGenerateMessage] = useState("");

  useEffect(() => {
    const loadRiskData = async () => {
      try {
        setLoading(true);
        setError("");

        const [riskResponse, sensorResponse, historyResponse] =
          await Promise.all([
            apiClient.get(
              `/gis/map-data/${RISK_ZONE_ID}`
            ),

            apiClient.get("/sensors"),

            apiClient.get(
              `/risk-assessments/history/${RISK_ZONE_ID}?limit=20`
            ),
          ]);

        const sensorList = sensorResponse.data;

        let latestSensor = null;

        if (sensorList.length > 0) {
          const sensor = sensorList[0];

          try {
            const readingResponse =
              await apiClient.get(
                `/sensor-readings/${sensor.public_id}/latest`
              );

            latestSensor = {
              ...sensor,
              latest_reading: readingResponse.data,
            };
          } catch (err) {
            if (err?.response?.status === 404) {
              latestSensor = {
                ...sensor,
                latest_reading: null,
              };
            } else {
              throw err;
            }
          }
        }

        setRiskData(riskResponse.data);
        setSensorData(latestSensor);
        setAssessmentHistory(historyResponse.data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load risk monitoring data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadRiskData();
  }, []);

  const generateFreshAssessment = async () => {
    try {
      setGenerating(true);
      setGenerateMessage("");
      setError("");

      const response = await apiClient.post(
        `/risk-assessments/generate/${RISK_ZONE_ID}?forecast_horizon_minutes=1440`
      );

      setGenerateMessage(
        `Fresh assessment generated: ${response.data.risk_probability_percent}% risk (${response.data.severity}).`
      );

      const [refreshedRiskData, refreshedHistory] =
        await Promise.all([
          apiClient.get(
            `/gis/map-data/${RISK_ZONE_ID}`
          ),

          apiClient.get(
            `/risk-assessments/history/${RISK_ZONE_ID}?limit=20`
          ),
        ]);

      setRiskData(
        refreshedRiskData.data
      );

      setAssessmentHistory(
        refreshedHistory.data
      );
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to generate fresh risk assessment."
      );
    } finally {
      setGenerating(false);
    }
  };

  const assessment = useMemo(() => {
    return (
      riskData?.latest_risk_assessment ??
      null
    );
  }, [riskData]);

  const reading = useMemo(() => {
    return (
      sensorData?.latest_reading ??
      null
    );
  }, [sensorData]);

  const satelliteObservation = useMemo(() => {
    return (
      riskData?.latest_satellite_observation ??
      null
    );
  }, [riskData]);

  const horizonHours = useMemo(() => {
    if (
      assessment?.forecast_horizon_minutes ===
        null ||
      assessment?.forecast_horizon_minutes ===
        undefined
    ) {
      return null;
    }

    return (
      assessment.forecast_horizon_minutes /
      60
    );
  }, [assessment]);

  const isExpired = useMemo(() => {
    if (!assessment?.valid_until) {
      return false;
    }

    return (
      new Date(assessment.valid_until) <
      new Date()
    );
  }, [assessment]);

  const isTestData = useMemo(() => {
    const zoneCode =
      riskData?.risk_zone?.zone_code
        ?.toLowerCase() || "";

    const modelName =
      assessment?.model_name
        ?.toLowerCase() || "";

    return (
      zoneCode.startsWith("test") ||
      modelName.startsWith("test")
    );
  }, [riskData, assessment]);

  const assessmentLabel = useMemo(() => {
    if (isTestData) {
      return "TEST / CONTROLLED ASSESSMENT";
    }

    if (isExpired) {
      return "HISTORICAL / EXPIRED ASSESSMENT";
    }

    return "LATEST AVAILABLE ASSESSMENT";
  }, [
    isTestData,
    isExpired,
  ]);

  const formatDateTime = (value) => {
    if (!value) {
      return "N/A";
    }

    return new Date(value).toLocaleString();
  };

  const formatValue = (
    value,
    unit = ""
  ) => {
    if (
      value === null ||
      value === undefined
    ) {
      return "N/A";
    }

    return `${value}${unit}`;
  };

  const getSeverityClass = (severity) => {
    if (!severity) {
      return "";
    }

    return `history-severity-${severity.toLowerCase()}`;
  };

  if (loading) {
    return (
      <div className="risk-monitor-state">
        Loading risk intelligence...
      </div>
    );
  }

  if (error) {
    return (
      <div className="risk-monitor-state risk-monitor-error">
        {error}
      </div>
    );
  }

  return (
    <main className="risk-monitor-page">

      <section className="risk-monitor-header">
        <div>
          <span className="section-kicker">
            AI RISK ENGINE
          </span>

          <h1>
            Risk Monitoring
          </h1>

          <p>
            Risk assessment record for{" "}
            <strong>
              {riskData?.risk_zone?.name ||
                "Unknown Risk Zone"}
            </strong>
          </p>
        </div>

        <div
          className={`assessment-status ${
            isExpired
              ? "expired"
              : "valid"
          }`}
        >
          {assessmentLabel}
        </div>
      </section>

      <section className="risk-monitor-grid">

        <article className="risk-monitor-card risk-high">
          <span>
            Risk Probability
          </span>

          <strong>
            {assessment?.risk_probability_percent ??
              "N/A"}%
          </strong>

          <p>
            Recorded model hazard probability
          </p>
        </article>

        <article className="risk-monitor-card risk-high">
          <span>
            Severity
          </span>

          <strong>
            {assessment?.severity ??
              "UNKNOWN"}
          </strong>

          <p>
            Recorded assessment classification
          </p>
        </article>

        <article className="risk-monitor-card">
          <span>
            Confidence
          </span>

          <strong>
            {assessment?.confidence_percent ??
              "N/A"}%
          </strong>

          <p>
            Model confidence score
          </p>
        </article>

        <article className="risk-monitor-card">
          <span>
            Forecast Horizon
          </span>

          <strong>
            {horizonHours !== null
              ? `${horizonHours} hr`
              : "N/A"}
          </strong>

          <p>
            Prediction window
          </p>
        </article>

      </section>

      <section className="risk-generation-panel">
        <div>
          <span className="section-kicker">
            RISK ASSESSMENT CONTROL
          </span>

          <h2>
            Generate Fresh Assessment
          </h2>

          <p>
            Recalculate the current hazard probability
            using the latest fused sensor, satellite,
            weather, terrain and historical inputs.
          </p>
        </div>

        <button
          type="button"
          className="generate-risk-button"
          onClick={generateFreshAssessment}
          disabled={generating}
        >
          {generating
            ? "Generating Assessment..."
            : "Generate Fresh Assessment"}
        </button>
      </section>

      {generateMessage && (
        <div className="risk-generation-success">
          {generateMessage}
        </div>
      )}

      <section className="risk-detail-panel risk-inputs-panel">

        <div className="risk-detail-heading">
          <span className="section-kicker">
            LIVE FUSED INPUTS
          </span>

          <h2>
            Risk Engine Inputs
          </h2>
        </div>

        <div className="risk-input-grid">

          <div className="risk-input-item">
            <span>Rainfall Rate</span>
            <strong>
              {formatValue(
                reading?.rainfall_rate_mm_hr,
                " mm/hr"
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Soil Moisture</span>
            <strong>
              {formatValue(
                reading?.soil_moisture_percent,
                "%"
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Slope</span>
            <strong>
              {formatValue(
                riskData?.risk_zone
                  ?.slope_degrees,
                "°"
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Satellite NDWI</span>
            <strong>
              {formatValue(
                satelliteObservation?.ndwi
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Satellite Soil Index</span>
            <strong>
              {formatValue(
                satelliteObservation
                  ?.soil_moisture_index
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Satellite NDVI</span>
            <strong>
              {formatValue(
                satelliteObservation?.ndvi
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Temperature</span>
            <strong>
              {formatValue(
                reading?.temperature_c,
                "°C"
              )}
            </strong>
          </div>

          <div className="risk-input-item">
            <span>Humidity</span>
            <strong>
              {formatValue(
                reading?.humidity_percent,
                "%"
              )}
            </strong>
          </div>

        </div>

        <div className="risk-input-source">
          <span>
            Sensor:{" "}
            {sensorData?.sensor_code ||
              "N/A"}
          </span>

          <span>
            Data quality:{" "}
            {reading
              ?.data_quality_status ||
              "N/A"}
          </span>

          <span>
            Received:{" "}
            {formatDateTime(
              reading?.received_at
            )}
          </span>
        </div>

      </section>

      <section className="risk-intelligence-grid">

        <article className="risk-detail-panel">

          <div className="risk-detail-heading">
            <span className="section-kicker">
              MODEL INTELLIGENCE
            </span>

            <h2>
              Assessment Details
            </h2>
          </div>

          <div className="risk-detail-list">

            <div>
              <span>Dominant Factor</span>

              <strong>
                {assessment
                  ?.dominant_factor ||
                  "N/A"}
              </strong>
            </div>

            <div>
              <span>Model</span>

              <strong>
                {assessment
                  ?.model_name ||
                  "N/A"}
              </strong>
            </div>

            <div>
              <span>Model Version</span>

              <strong>
                {assessment
                  ?.model_version ||
                  "N/A"}
              </strong>
            </div>

            <div>
              <span>Assessed At</span>

              <strong>
                {formatDateTime(
                  assessment?.assessed_at
                )}
              </strong>
            </div>

            <div>
              <span>Valid Until</span>

              <strong>
                {formatDateTime(
                  assessment?.valid_until
                )}
              </strong>
            </div>

          </div>

        </article>

        <article className="risk-detail-panel">

          <div className="risk-detail-heading">
            <span className="section-kicker">
              AI EXPLANATION
            </span>

            <h2>
              Risk Interpretation
            </h2>
          </div>

          <div className="risk-explanation">

            <div className="factor-badge">
              Dominant Factor:{" "}
              {assessment
                ?.dominant_factor ||
                "Unknown"}
            </div>

            <p>
              {assessment?.explanation ||
                "No explanation is available for this assessment."}
            </p>

          </div>

        </article>

      </section>

      <section className="risk-history-panel">

        <div className="risk-detail-heading">
          <span className="section-kicker">
            HISTORICAL INTELLIGENCE
          </span>

          <h2>
            Assessment History
          </h2>

          <p className="risk-history-description">
            Previous risk assessments generated for
            this monitoring zone.
          </p>
        </div>

        {assessmentHistory.length === 0 ? (
          <div className="risk-history-empty">
            No previous risk assessments available.
          </div>
        ) : (
          <div className="risk-history-table-wrapper">
            <table className="risk-history-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Risk</th>
                  <th>Severity</th>
                  <th>Confidence</th>
                  <th>Horizon</th>
                  <th>Dominant Factor</th>
                </tr>
              </thead>

              <tbody>
                {assessmentHistory.map(
                  (item) => (
                    <tr key={item.public_id}>

                      <td>
                        {formatDateTime(
                          item.assessed_at
                        )}
                      </td>

                      <td className="history-risk-value">
                        {item.risk_probability_percent}%
                      </td>

                      <td>
                        <span
                          className={`history-severity ${getSeverityClass(
                            item.severity
                          )}`}
                        >
                          {item.severity}
                        </span>
                      </td>

                      <td>
                        {item.confidence_percent !==
                        null
                          ? `${item.confidence_percent}%`
                          : "N/A"}
                      </td>

                      <td>
                        {item.forecast_horizon_minutes /
                          60} hr
                      </td>

                      <td>
                        {item.dominant_factor ||
                          "N/A"}
                      </td>

                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        )}

      </section>

    </main>
  );
}
