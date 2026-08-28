import L from "leaflet";

import {
  CircleMarker,
  MapContainer,
  Marker,
  Popup,
  Polyline,
  TileLayer,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";


const villageIcon = L.divIcon({
  className: "",
  html: `
    <div style="
      width: 22px;
      height: 22px;
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg);
      background: #0ea5e9;
      border: 3px solid #e0f2fe;
      box-shadow: 0 0 14px rgba(14,165,233,0.7);
      position: relative;
    ">
      <div style="
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #ffffff;
        position: absolute;
        top: 5px;
        left: 5px;
      "></div>
    </div>
  `,
  iconSize: [22, 22],
  iconAnchor: [11, 22],
  popupAnchor: [0, -20],
});


function getRiskStyle(severity) {
  switch ((severity || "").toUpperCase()) {
    case "CRITICAL":
      return {
        color: "#991b1b",
        fillColor: "#dc2626",
      };

    case "HIGH":
      return {
        color: "#dc2626",
        fillColor: "#ef4444",
      };

    case "MODERATE":
    case "MEDIUM":
      return {
        color: "#d97706",
        fillColor: "#f59e0b",
      };

    case "LOW":
      return {
        color: "#15803d",
        fillColor: "#22c55e",
      };

    default:
      return {
        color: "#0369a1",
        fillColor: "#0ea5e9",
      };
  }
}


export default function HazardMap({
  riskZone,
  villages = [],
  roadSegments = [],
  latestRiskAssessment,
}) {
  if (!riskZone) {
    return <div>Risk zone data unavailable.</div>;
  }

  const center = [
    riskZone.latitude,
    riskZone.longitude,
  ];

  const riskScore =
    latestRiskAssessment?.risk_probability_percent ?? null;

  const severity =
    latestRiskAssessment?.severity ?? "UNKNOWN";

  const riskStyle = getRiskStyle(severity);

  return (
    <MapContainer
      center={center}
      zoom={12}
      scrollWheelZoom
      style={{
        height: "500px",
        width: "100%",
        borderRadius: "12px",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <CircleMarker
        center={center}
        radius={20}
        pathOptions={{
          color: riskStyle.color,
          fillColor: riskStyle.fillColor,
          fillOpacity: 0.5,
          weight: 4,
        }}
      >
        <Popup>
          <strong>{riskZone.name}</strong>
          <br />
          {riskZone.district}, {riskZone.state}
          <br />
          Severity: {severity}
          <br />
          Risk: {riskScore !== null ? `${riskScore}%` : "N/A"}
          <br />
          Slope:{" "}
          {riskZone.slope_degrees !== null &&
          riskZone.slope_degrees !== undefined
            ? `${riskZone.slope_degrees}�`
            : "N/A"}
        </Popup>
      </CircleMarker>

      {villages.map((village) => (
        <Marker
          key={village.public_id}
          position={[
            village.latitude,
            village.longitude,
          ]}
          icon={villageIcon}
        >
          <Popup>
            <strong>{village.name}</strong>
            <br />
            {village.district}, {village.state}
            <br />
            Population: {village.population ?? "N/A"}
            <br />
            Accessible: {village.is_accessible ? "Yes" : "No"}
            <br />
            Health Facility:{" "}
            {village.has_health_facility ? "Yes" : "No"}
            <br />
            School: {village.has_school ? "Yes" : "No"}
          </Popup>
        </Marker>
      ))}

      {roadSegments.map((road) => (
        <Polyline
          key={road.public_id}
          positions={[
            [
              road.start_latitude,
              road.start_longitude,
            ],
            [
              road.end_latitude,
              road.end_longitude,
            ],
          ]}
          pathOptions={{
            color: road.is_blocked ? "#dc2626" : "#16a34a",
            weight: road.is_blocked ? 6 : 4,
            opacity: 0.95,
            dashArray: road.is_blocked ? "10 8" : null,
          }}
        >
          <Popup>
            <strong>{road.name}</strong>
            <br />
            Type: {road.road_type}
            <br />
            Length:{" "}
            {road.length_km !== null &&
            road.length_km !== undefined
              ? `${road.length_km} km`
              : "N/A"}
            <br />
            Status: {road.is_blocked ? "Blocked" : "Open"}
            {road.is_blocked && road.blockage_reason ? (
              <>
                <br />
                Reason: {road.blockage_reason}
              </>
            ) : null}
          </Popup>
        </Polyline>
      ))}
    </MapContainer>
  );
}
