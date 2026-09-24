import requests
from datetime import datetime, timedelta


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude, longitude):
    now = datetime.now()
    start_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = now.strftime("%Y-%m-%d")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "rain"
        ],
        "hourly": [
            "rain"
        ],
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()
    current = data["current"]

    hourly_times = data["hourly"]["time"]
    hourly_rain = data["hourly"]["rain"]

    current_time = datetime.fromisoformat(current["time"])
    cutoff_time = current_time - timedelta(hours=24)

    rain_24h = 0.0

    for time_str, rain_value in zip(hourly_times, hourly_rain):
        hour_time = datetime.fromisoformat(time_str)

        if cutoff_time <= hour_time <= current_time:
            rain_24h += rain_value or 0.0

    return {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "rain": current["rain"],
        "rain_24h": round(rain_24h, 2),
        "timestamp": current["time"]
    }
