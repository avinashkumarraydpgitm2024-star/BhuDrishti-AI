def map_weather_features(weather_data, terrain_data=None, soil_data=None):
    required_fields = [
        "temperature",
        "humidity",
        "rain_24h"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in weather_data
    ]

    if missing_fields:
        raise ValueError(
            f"Missing weather fields: {', '.join(missing_fields)}"
        )

    result = {
        "rainfall": float(weather_data["rain_24h"]),
        "temperature": float(weather_data["temperature"]),
        "humidity": float(weather_data["humidity"])
    }

    if terrain_data is not None:
        result["slope"] = float(terrain_data["slope_degrees"])

    if soil_data is not None:
        result["soil_moisture_m3_m3"] = float(
            soil_data["soil_moisture_m3_m3"]
        )

    return result


