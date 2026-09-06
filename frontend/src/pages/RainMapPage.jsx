import { useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";

import {
  Circle,
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";

import L from "leaflet";

import apiClient from "../api/client";

import "./RainMapPage.css";

import "leaflet/dist/leaflet.css";

const DEFAULT_ZONE_ID = "fe1f520f-e8a0-40bd-9eb1-c876502a28d1";
const DEFAULT_LATITUDE = 27.3314;
const DEFAULT_LONGITUDE = 88.6138;

function MapController({ latitude, longitude }) {
  const map = useMap();

  useEffect(() => {
    if (
      latitude === null ||
      latitude === undefined ||
      longitude === null ||
      longitude === undefined
    ) {
      return;
    }

    map.setView(
      [Number(latitude), Number(longitude)],
      11,
      { animate: true }
    );
  }, [map, latitude, longitude]);

  return null;
}

function formatNumber(value, digits = 1) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  const number = Number(value);

  if (Number.isNaN(number)) {
    return "N/A";
  }

  return number.toFixed(digits);
}


function formatTime(value) {
  if (!value) {
    return "N/A";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "N/A";
  }

  return date.toLocaleString();
}


function getRainIntensity(rate) {
  const value = Number(rate || 0);

  if (value <= 0) {
    return {
      label: "No Rain",
      className: "none",
    };
  }

  if (value < 2.5) {
    return {
      label: "Light Rain",
      className: "light",
    };
  }

  if (value < 7.5) {
    return {
      label: "Moderate Rain",
      className: "moderate",
    };
  }

  if (value < 15) {
    return {
      label: "Heavy Rain",
      className: "heavy",
    };
  }

  return {
    label: "Very Heavy Rain",
    className: "extreme",
  };
}


export default function RainMapPage() {
  const [searchParams, setSearchParams] =
    useSearchParams();

  const [dashboard, setDashboard] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [searchLocation, setSearchLocation] =
    useState(
      searchParams.get("location") || ""
    );

  const [userLocation, setUserLocation] =
    useState(null);

  const [mapLocation, setMapLocation] =
    useState({
      latitude: DEFAULT_LATITUDE,
      longitude: DEFAULT_LONGITUDE,
    });

  const [locationStatus, setLocationStatus] =
    useState("");

  const [locationLoading, setLocationLoading] =
    useState(false);


  const loadRainData = useCallback(
    async () => {
      try {
        setLoading(true);
        setError("");

        const latitude = Number(mapLocation.latitude);
        const longitude = Number(mapLocation.longitude);

        const zoneResponse = await apiClient.get(
          `/gis/map-data/${DEFAULT_ZONE_ID}`
        );

        const currentResponse = await apiClient.post(
          `/weather/sync-current?latitude=${latitude}&longitude=${longitude}`
        );

        const forecastResponse = await apiClient.post(
          `/weather/sync-forecast?latitude=${latitude}&longitude=${longitude}&forecast_days=7`
        );

        setDashboard({
          ...zoneResponse.data,
          current_weather: currentResponse.data,
          weather_forecasts: forecastResponse.data,
        });
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
            "Unable to load live rainfall data."
        );
      } finally {
        setLoading(false);
      }
    },
    [mapLocation.latitude, mapLocation.longitude]
  );


  useEffect(() => {
    loadRainData();

    const interval = setInterval(
      loadRainData,
      60000
    );

    return () => clearInterval(interval);
  }, [loadRainData]);


  const currentWeather =
    dashboard?.current_weather || null;


  const forecasts =
    dashboard?.weather_forecasts || [];


  const currentRainRate =
    currentWeather?.rainfall_rate_mm_hr ??
    0;


  const currentRainfall =
    currentWeather?.rainfall_mm ??
    0;


  const intensity =
    useMemo(
      () =>
        getRainIntensity(
          currentRainRate
        ),
      [currentRainRate]
    );


  const forecastTotal =
    useMemo(
      () =>
        forecasts
          .slice(0, 24)
          .reduce(
            (total, item) =>
              total +
              Number(
                item?.precipitation_mm || 0
              ),
            0
          ),
      [forecasts]
    );


  const maximumProbability =
    useMemo(() => {
      const values =
        forecasts
          .slice(0, 24)
          .map(
            (item) =>
              Number(
                item?.precipitation_probability_percent
              )
          )
          .filter(
            (value) =>
              !Number.isNaN(value)
          );

      return values.length
        ? Math.max(...values)
        : null;
    }, [forecasts]);


  const useMyLocation = () => {
    if (!navigator.geolocation) {
      setLocationStatus(
        "Geolocation is not supported by this browser."
      );

      return;
    }

    setLocationLoading(true);

    setLocationStatus(
      "Detecting your current location..."
    );

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude =
          position.coords.latitude;

        const longitude =
          position.coords.longitude;

        setUserLocation({
          latitude,
          longitude,
        });

        setLocationStatus(
          `Location detected: ${latitude.toFixed(
            4
          )}, ${longitude.toFixed(4)}`
        );

        setLocationLoading(false);
      },

      (locationError) => {
        if (
          locationError.code ===
          locationError.PERMISSION_DENIED
        ) {
          setLocationStatus(
            "Location permission was denied."
          );
        } else {
          setLocationStatus(
            "Unable to determine your location."
          );
        }

        setLocationLoading(false);
      },

      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000,
      }
    );
  };


  const handleSearch = async (event) => {
    event.preventDefault();

    const query = searchLocation.trim();

    if (!query) {
      setLocationStatus(
        "Enter a location to search."
      );
      return;
    }

    setSearchParams({
      location: query,
    });

    setLocationStatus(
      `Searching location "${query}"...`
    );

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error("Location search failed.");
      }

      const results = await response.json();

      if (!results.length) {
        setLocationStatus(
          `Location "${query}" was not found.`
        );
        return;
      }

      const latitude = Number(results[0].lat);
      const longitude = Number(results[0].lon);

      setMapLocation({
        latitude,
        longitude,
      });

      setLocationStatus(
        `Location found: ${query}`
      );
    } catch (searchError) {
      setLocationStatus(
        "Unable to search this location right now."
      );
    }
  };


  if (loading && !dashboard) {
    return (
      <main className="rain-page-state">
        <div className="rain-loader" />

        <h2>
          Loading live rain intelligence...
        </h2>

        <p>
          Connecting to the latest weather
          observation and forecast.
        </p>
      </main>
    );
  }


  if (error && !dashboard) {
    return (
      <main className="rain-page-state rain-error">
        <h2>
          Rain intelligence unavailable
        </h2>

        <p>{error}</p>

        <button
          type="button"
          onClick={loadRainData}
        >
          Try Again
        </button>
      </main>
    );
  }


  return (
    <main className="rain-page">

      {/* =====================================================
          HEADER
          ===================================================== */}

      <section className="rain-page-header">

        <div>

          <span className="rain-kicker">
            LIVE WEATHER INTELLIGENCE
          </span>

          <h1>
            Rain Status & Map
          </h1>

          <p>
            Monitor current rainfall conditions
            and precipitation forecasts across
            monitored hazard zones.
          </p>

        </div>


        <div className="rain-live-indicator">

          <span />

          LIVE DATA

        </div>

      </section>


      {/* =====================================================
          LOCATION SEARCH
          ===================================================== */}

      <section className="rain-location-card">

        <div className="rain-location-title">

          <div>

            <span>
              LOCATION SEARCH
            </span>

            <h3>
              Check rainfall for a location
            </h3>

          </div>

          <div className="rain-location-symbol">
            
          </div>

        </div>


        <form
          className="rain-search-form"
          onSubmit={handleSearch}
        >

          <input
            type="search"
            value={searchLocation}
            onChange={(event) =>
              setSearchLocation(
                event.target.value
              )
            }
            placeholder="Search village, city, district or location..."
            aria-label="Search rainfall location"
          />


          <button type="submit">
            Search
          </button>

        </form>


        <div className="rain-location-actions">

          <button
            type="button"
            onClick={useMyLocation}
            disabled={locationLoading}
            className="rain-my-location"
          >
            {locationLoading
              ? "Detecting..."
              : " Use My Location"}
          </button>


          <span>
            {locationStatus ||
              "Allow location access to use your device position."}
          </span>

        </div>


        {userLocation && (
          <div className="rain-detected-location">

            <span>
              DEVICE LOCATION
            </span>

            <strong>
              {userLocation.latitude.toFixed(
                5
              )}
              {" , "}
              {userLocation.longitude.toFixed(
                5
              )}
            </strong>

          </div>
        )}

      </section>


      {/* =====================================================
          CURRENT RAIN METRICS
          ===================================================== */}

      <section className="rain-metrics">

        <article className="rain-metric-card primary">

          <div className="rain-metric-label">
            CURRENT RAIN RATE
          </div>

          <strong>
            {formatNumber(
              currentRainRate,
              1
            )}
            <small>
              {" "}mm/hr
            </small>
          </strong>

          <span
            className={`rain-intensity-badge ${intensity.className}`}
          >
            {intensity.label}
          </span>

        </article>


        <article className="rain-metric-card">

          <div className="rain-metric-label">
            OBSERVED RAINFALL
          </div>

          <strong>
            {formatNumber(
              currentRainfall,
              1
            )}
            <small>
              {" "}mm
            </small>
          </strong>

          <span>
            Latest observation
          </span>

        </article>


        <article className="rain-metric-card">

          <div className="rain-metric-label">
            NEXT 24H RAINFALL
          </div>

          <strong>
            {formatNumber(
              forecastTotal,
              1
            )}
            <small>
              {" "}mm
            </small>
          </strong>

          <span>
            Forecast precipitation
          </span>

        </article>


        <article className="rain-metric-card">

          <div className="rain-metric-label">
            RAIN PROBABILITY
          </div>

          <strong>
            {maximumProbability !== null
              ? `${formatNumber(
                  maximumProbability,
                  0
                )}%`
              : "N/A"}
          </strong>

          <span>
            Maximum next 24h probability
          </span>

        </article>

      </section>


      {/* =====================================================
          MAP AREA
          ===================================================== */}

      <section className="rain-map-card">

        <div className="rain-map-header">

          <div>

            <span className="rain-kicker">
              GEOSPATIAL RAINFALL
            </span>

            <h2>
              Live Rainfall Map
            </h2>

            <p>
              Current monitored location and
              rainfall intensity.
            </p>

          </div>


          <div className="rain-map-source">

            <span>
              SOURCE
            </span>

            <strong>
              {currentWeather?.provider ||
                "Open-Meteo"}
            </strong>

          </div>

        </div>


                <div className="rain-map-container">

          <MapContainer
            center={[
              Number(
                mapLocation.latitude
              ),
              Number(
                mapLocation.longitude
              ),
            ]}
            zoom={11}
            scrollWheelZoom={true}
            className="rain-leaflet-map"
          >

            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <MapController
              latitude={
                mapLocation.latitude
              }
              longitude={
                mapLocation.longitude
              }
            />

            <Circle
              center={[
                Number(
                  mapLocation.latitude
                ),
                Number(
                  mapLocation.longitude
                ),
              ]}
              radius={1500}
              pathOptions={{
                color:
                  intensity.className === "extreme"
                    ? "#d9534f"
                    : intensity.className === "heavy"
                      ? "#e67e22"
                      : intensity.className === "moderate"
                        ? "#f6b93b"
                        : "#1677c8",
                fillOpacity: 0.18,
              }}
            />

            <Marker
              position={[
                Number(
                  mapLocation.latitude
                ),
                Number(
                  mapLocation.longitude
                ),
              ]}
            >

              <Popup>

                <strong>
                  {dashboard?.risk_zone?.name ||
                    "Monitored Zone"}
                </strong>

                <br />

                Rain Rate:{" "}
                {formatNumber(
                  currentRainRate,
                  1
                )}{" "}
                mm/hr

                <br />

                Rainfall:{" "}
                {formatNumber(
                  currentRainfall,
                  1
                )}{" "}
                mm

                <br />

                Intensity:{" "}
                {intensity.label}

              </Popup>

            </Marker>

          </MapContainer>

        </div></section>


      {/* =====================================================
          WEATHER DETAILS
          ===================================================== */}

      <section className="rain-weather-grid">

        <article className="rain-weather-card">

          <span>
            TEMPERATURE
          </span>

          <strong>
            {formatNumber(
              currentWeather?.temperature_c,
              1
            )}
            C
          </strong>

        </article>


        <article className="rain-weather-card">

          <span>
            HUMIDITY
          </span>

          <strong>
            {formatNumber(
              currentWeather?.humidity_percent,
              0
            )}
            %
          </strong>

        </article>


        <article className="rain-weather-card">

          <span>
            WIND
          </span>

          <strong>
            {formatNumber(
              currentWeather?.wind_speed_mps,
              1
            )}
            m/s
          </strong>

        </article>


        <article className="rain-weather-card">

          <span>
            PRESSURE
          </span>

          <strong>
            {formatNumber(
              currentWeather?.atmospheric_pressure_hpa,
              1
            )}
            hPa
          </strong>

        </article>

      </section>


      {/* =====================================================
          FORECAST
          ===================================================== */}

      <section className="rain-forecast-card">

        <div className="rain-map-header">

          <div>

            <span className="rain-kicker">
              PRECIPITATION FORECAST
            </span>

            <h2>
              Upcoming Rainfall
            </h2>

          </div>

          <span className="rain-forecast-count">
            {forecasts.length} forecast points
          </span>

        </div>


        <div className="rain-forecast-list">

          {forecasts
            .slice(0, 12)
            .map((forecast) => (
              <div
                className="rain-forecast-item"
                key={forecast.public_id}
              >

                <span>
                  {new Date(
                    forecast.forecast_for
                  ).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>

                <strong>
                  {formatNumber(
                    forecast.precipitation_mm,
                    1
                  )}{" "}
                  mm
                </strong>

                <small>
                  {formatNumber(
                    forecast.precipitation_probability_percent,
                    0
                  )}
                  %
                </small>

              </div>
            ))}

        </div>

      </section>

    </main>
  );
}
