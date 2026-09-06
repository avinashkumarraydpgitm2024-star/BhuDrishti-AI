import { useMemo } from "react";
import Map, { Layer, Marker, NavigationControl, Popup, Source } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";

function riskColor(severity) {
  switch (String(severity || "").toUpperCase()) {
    case "CRITICAL": return "#ef4444";
    case "HIGH": return "#ff5b63";
    case "MODERATE":
    case "MEDIUM": return "#f5c344";
    case "LOW": return "#2bd58d";
    default: return "#20b8f2";
  }
}

const MAP_STYLE = {
  version: 8,
  sources: {
    osm: {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "Â© OpenStreetMap contributors"
    },
    terrain: {
      type: "raster-dem",
      url: "https://demotiles.maplibre.org/terrain-tiles/tiles.json",
      tileSize: 256
    }
  },
  layers: [{
    id: "osm",
    type: "raster",
    source: "osm",
    paint: {
      "raster-saturation": -0.35,
      "raster-contrast": 0.15,
      "raster-brightness-max": 0.82
    }
  }],
  terrain: {
    source: "terrain",
    exaggeration: 1.35
  }
};

export default function HazardMap({ riskZone, villages = [], roadSegments = [], latestRiskAssessment }) {
  if (!riskZone) return <div>Risk zone data unavailable.</div>;

  const latitude = Number(riskZone.latitude);
  const longitude = Number(riskZone.longitude);
  const severity = latestRiskAssessment?.severity || "UNKNOWN";
  const score = latestRiskAssessment?.risk_probability_percent ?? null;
  const color = riskColor(severity);

  const roads = useMemo(() => ({
    type: "FeatureCollection",
    features: roadSegments
      .filter(r => [r.start_latitude,r.start_longitude,r.end_latitude,r.end_longitude].every(v => Number.isFinite(Number(v))))
      .map(r => ({
        type: "Feature",
        properties: { blocked: Boolean(r.is_blocked) },
        geometry: {
          type: "LineString",
          coordinates: [
            [Number(r.start_longitude), Number(r.start_latitude)],
            [Number(r.end_longitude), Number(r.end_latitude)]
          ]
        }
      }))
  }), [roadSegments]);

  return (
    <div className="hazard-map-3d">
      <Map
        initialViewState={{ longitude, latitude, zoom: 10.8, pitch: 58, bearing: -18 }}
        mapStyle={MAP_STYLE}
        maxPitch={75}
        dragRotate
        touchPitch
        scrollZoom
        style={{ width: "100%", height: "100%" }}
      >
        <NavigationControl position="top-right" showCompass />
        <Source id="roads" type="geojson" data={roads}>
          <Layer id="roads-open" type="line" filter={["==",["get","blocked"],false]}
            paint={{"line-color":"#25d58d","line-width":3.5,"line-opacity":0.92}} />
          <Layer id="roads-blocked" type="line" filter={["==",["get","blocked"],true]}
            paint={{"line-color":"#ff4f62","line-width":5,"line-opacity":0.95,"line-dasharray":[2,2]}} />
        </Source>

        <Marker longitude={longitude} latitude={latitude} anchor="center">
          <div className="risk-3d-marker" style={{"--risk-color": color}}><span /></div>
        </Marker>

        {villages.map(v => (
          <Marker key={v.public_id} longitude={Number(v.longitude)} latitude={Number(v.latitude)} anchor="bottom">
            <div className="village-3d-marker" title={v.name} />
          </Marker>
        ))}

        <Popup longitude={longitude} latitude={latitude} closeButton={false} closeOnClick={false} anchor="bottom" offset={18}>
          <div className="hazard-popup">
            <strong>{riskZone.name}</strong>
            <span>{riskZone.district}, {riskZone.state}</span>
            <span>Severity: <b>{severity}</b></span>
            <span>Risk: <b>{score !== null ? `${score}%` : "N/A"}</b></span>
          </div>
        </Popup>
      </Map>

      <div className="map-3d-badge"><span className="map-3d-pulse" />3D TERRAIN</div>
      <div className="map-3d-hint">Drag to rotate Â· Scroll to zoom</div>
    </div>
  );
}
