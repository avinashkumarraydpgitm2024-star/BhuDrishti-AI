import requests


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_soil_moisture(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "soil_moisture_0_to_1cm",
            "soil_moisture_1_to_3cm",
            "soil_moisture_3_to_9cm"
        ],
        "timezone": "auto"
    }

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()
    current = data["current"]

    values = [
        current["soil_moisture_0_to_1cm"],
        current["soil_moisture_1_to_3cm"],
        current["soil_moisture_3_to_9cm"]
    ]

    average_m3_m3 = sum(values) / len(values)

    return {
        "latitude": float(data["latitude"]),
        "longitude": float(data["longitude"]),
        "soil_moisture_m3_m3": round(average_m3_m3, 4),
        "timestamp": current["time"]
    }
