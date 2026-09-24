import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "rain"
        ],
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

    return {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "rain": current["rain"],
        "timestamp": current["time"]
    }
