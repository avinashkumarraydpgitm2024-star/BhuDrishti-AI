import { useEffect, useMemo, useState } from "react";

import apiClient from "../api/client";

import "./RiskMonitoringPage.css";


const RISK_ZONE_ID = "fe1f520f-e8a0-40bd-9eb1-c876502a28d1";


export default function RiskMonitoringPage() {
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const loadRiskData = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await apiClient.get(
          `/gis/map-data/${RISK_ZONE_ID}`
        );

        setRiskData(response.data);
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


  const assessment = useMemo(() => {
    return riskData?.latest_risk_assessment ?? null;
  }, [riskData]);


  const horizonHours = useMemo(() => {
    if (
      assessment?.forecast_horizon_minutes === null ||
      assessment?.forecast_horizon_minutes === undefined
    ) {
      return null;
    }

    return assessment.forecast_horizon_minutes / 60;
  }, [assessment]);


  const isExpired = useMemo(() => {
    if (!assessment?.valid_until) {
      return false;
    }

    return new Date(assessment.valid_until) < new Date();
  }, [assessment]);


  const isTestData = useMemo(() => {
    const zoneCode =
      riskData?.risk_zone?.zone_code?.toLowerCase() || "";

    const modelName =
      assessment?.model_name?.toLowerCase() || "";

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
  }, [isTestData, isExpired]);



  const formatDateTime = (value) => {
    if (!value) {
      return "N/A";
    }

    return new Date(value).toLocaleString();
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

          <h1>Risk Monitoring</h1>

          <p>
            Risk assessment record for{" "}
            <strong>{riskData.risk_zone.name}</strong>
          </p>
        </div>

        <div
          className={`assessment-status ${
            isExpired ? "expired" : "valid"
          }`}
        >
          {assessmentLabel}
        </div>
      </section>


      <section className="risk-monitor-grid">
        <article className="risk-monitor-card risk-high">
          <span>Risk Probability</span>

          <strong>
            {assessment?.risk_probability_percent ?? "N/A"}%
          </strong>

          <p>Recorded model hazard probability</p>
        </article>


        <article className="risk-monitor-card risk-high">
          <span>Severity</span>

          <strong>
            {assessment?.severity ?? "UNKNOWN"}
          </strong>

          <p>Recorded assessment classification</p>
        </article>


        <article className="risk-monitor-card">
          <span>Confidence</span>

          <strong>
            {assessment?.confidence_percent ?? "N/A"}%
          </strong>

          <p>Model confidence score</p>
        </article>


        <article className="risk-monitor-card">
          <span>Forecast Horizon</span>

          <strong>
            {horizonHours !== null
              ? `${horizonHours} hr`
              : "N/A"}
          </strong>

          <p>Prediction window</p>
        </article>
      </section>


      <section className="risk-intelligence-grid">
        <article className="risk-detail-panel">
          <div className="risk-detail-heading">
            <span className="section-kicker">
              MODEL INTELLIGENCE
            </span>

            <h2>Assessment Details</h2>
          </div>

          <div className="risk-detail-list">
            <div>
              <span>Dominant Factor</span>
              <strong>
                {assessment?.dominant_factor || "N/A"}
              </strong>
            </div>

            <div>
              <span>Model</span>
              <strong>
                {assessment?.model_name || "N/A"}
              </strong>
            </div>

            <div>
              <span>Model Version</span>
              <strong>
                {assessment?.model_version || "N/A"}
              </strong>
            </div>

            <div>
              <span>Assessed At</span>
              <strong>
                {formatDateTime(assessment?.assessed_at)}
              </strong>
            </div>

            <div>
              <span>Valid Until</span>
              <strong>
                {formatDateTime(assessment?.valid_until)}
              </strong>
            </div>
          </div>
        </article>


        <article className="risk-detail-panel">
          <div className="risk-detail-heading">
            <span className="section-kicker">
              AI EXPLANATION
            </span>

            <h2>Risk Interpretation</h2>
          </div>

          <div className="risk-explanation">
            <div className="factor-badge">
              Dominant Factor:{" "}
              {assessment?.dominant_factor || "Unknown"}
            </div>

            <p>
              {assessment?.explanation ||
                "No explanation is available for this assessment."}
            </p>
          </div>
        </article>
      </section>
    </main>
  );
}




