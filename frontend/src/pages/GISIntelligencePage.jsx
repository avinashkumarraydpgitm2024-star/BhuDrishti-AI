import { useEffect, useMemo, useState } from "react";

import apiClient from "../api/client";
import HazardMap from "../components/map/HazardMap";

import "./GISIntelligencePage.css";


const RISK_ZONE_ID = "fe1f520f-e8a0-40bd-9eb1-c876502a28d1";


export default function GISIntelligencePage() {
  const [gisData, setGisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const loadGISData = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await apiClient.get(
          `/gis/map-data/${RISK_ZONE_ID}`
        );

        setGisData(response.data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Failed to load GIS intelligence data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadGISData();
  }, []);


  const riskScore = useMemo(() => {
    return (
      gisData?.latest_risk_assessment
        ?.risk_probability_percent ?? null
    );
  }, [gisData]);


  const severity = useMemo(() => {
    return (
      gisData?.latest_risk_assessment?.severity ||
      "UNKNOWN"
    );
  }, [gisData]);


  const isTestData = useMemo(() => {
    const zoneCode =
      gisData?.risk_zone?.zone_code?.toLowerCase() || "";

    const modelName =
      gisData?.latest_risk_assessment?.model_name?.toLowerCase() || "";

    return (
      zoneCode.startsWith("test") ||
      modelName.startsWith("test")
    );
  }, [gisData]);


  const isAssessmentExpired = useMemo(() => {
    const validUntil =
      gisData?.latest_risk_assessment?.valid_until;

    if (!validUntil) {
      return false;
    }

    return new Date(validUntil).getTime() < Date.now();
  }, [gisData]);


  const intelligenceStatus = useMemo(() => {
    if (isTestData) {
      return "TEST / CONTROLLED DATA";
    }

    if (isAssessmentExpired) {
      return "HISTORICAL / EXPIRED";
    }

    return "LATEST AVAILABLE DATA";
  }, [isTestData, isAssessmentExpired]);


  if (loading) {
    return (
      <div className="gis-state">
        Loading GIS intelligence...
      </div>
    );
  }


  if (error) {
    return (
      <div className="gis-state gis-error">
        {error}
      </div>
    );
  }


  return (
    <main className="gis-page">
      <section className="gis-header">
        <div>
          <span className="section-kicker">
            GEOSPATIAL INTELLIGENCE
          </span>

          <h1>GIS Intelligence</h1>

          <p>
            Spatial intelligence for{" "}
            <strong>{gisData.risk_zone.name}</strong>
          </p>
        </div>

        <div className="gis-risk-summary">
          <span>Latest Risk Assessment</span>

          <strong>
            {riskScore !== null
              ? `${riskScore}%`
              : "N/A"}
          </strong>

          <small>{severity}</small>
        </div>
      </section>


      <section className="gis-stat-grid">
        <article className="gis-stat-card">
          <span>Villages</span>
          <strong>{gisData.village_count}</strong>
          <p>Monitored settlements</p>
        </article>

        <article className="gis-stat-card">
          <span>Road Segments</span>
          <strong>{gisData.road_segment_count}</strong>
          <p>Mapped infrastructure links</p>
        </article>

        <article className="gis-stat-card">
          <span>Blocked Roads</span>
          <strong>{gisData.blocked_road_count}</strong>
          <p>Current accessibility disruptions</p>
        </article>

        <article className="gis-stat-card">
          <span>Active Alerts</span>
          <strong>{gisData.active_alert_count}</strong>
          <p>Unresolved hazard warnings</p>
        </article>
      </section>


      <section className="gis-map-panel">
        <div className="gis-panel-heading">
          <div>
            <span className="section-kicker">
              GIS MAP
            </span>

            <h2>Hazard & Infrastructure Map</h2>
          </div>

          <span className="gis-live-badge">
            {intelligenceStatus}
          </span>
        </div>

        <div className="gis-map-wrapper">
          <HazardMap
            riskZone={gisData.risk_zone}
            villages={gisData.villages}
            roadSegments={gisData.road_segments}
            latestRiskAssessment={
              gisData.latest_risk_assessment
            }
          />
        </div>

        <div className="gis-map-legend">
          <div>
            <span className="legend-dot danger" />
            Risk Zone
          </div>

          <div>
            <span className="legend-dot village" />
            Village
          </div>

          <div>
            <span className="legend-line open" />
            Open Road
          </div>

          <div>
            <span className="legend-line blocked" />
            Blocked Road
          </div>
        </div>
      </section>
    </main>
  );
}

