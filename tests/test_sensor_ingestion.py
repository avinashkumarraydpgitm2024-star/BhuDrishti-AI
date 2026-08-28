from datetime import datetime, timezone


def test_sensor_ingestion_requires_device_headers(client):
    response = client.post(
        "/api/v1/sensor-readings",
        json={
            "device_event_id": "pytest-security-event-001",
            "sensor_public_id": "00000000-0000-0000-0000-000000000000",
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 422

    detail = response.json()["detail"]
    missing_headers = {
        item["loc"][-1]
        for item in detail
        if item["type"] == "missing"
    }

    assert "X-Sensor-ID" in missing_headers
    assert "X-Device-API-Key" in missing_headers


def test_sensor_ingestion_rejects_invalid_device_credentials(client):
    response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": "00000000-0000-0000-0000-000000000000",
            "X-Device-API-Key": "invalid-device-api-key",
        },
        json={
            "device_event_id": "pytest-security-event-002",
            "sensor_public_id": "00000000-0000-0000-0000-000000000000",
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid device credentials."
    }


def test_sensor_ingestion_accepts_valid_device_credentials(
    client,
    provisioned_test_sensor,
):
    sensor, raw_api_key = provisioned_test_sensor

    response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": sensor.public_id,
            "X-Device-API-Key": raw_api_key,
        },
        json={
            "device_event_id": "pytest-valid-event-001",
            "sensor_public_id": sensor.public_id,
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["device_event_id"] == "pytest-valid-event-001"
    assert body["temperature_c"] == 20.0


def test_sensor_ingestion_rejects_duplicate_device_event(
    client,
    provisioned_test_sensor,
):
    sensor, raw_api_key = provisioned_test_sensor

    payload = {
        "device_event_id": "pytest-duplicate-event-001",
        "sensor_public_id": sensor.public_id,
        "temperature_c": 20.0,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    headers = {
        "X-Sensor-ID": sensor.public_id,
        "X-Device-API-Key": raw_api_key,
    }

    first_response = client.post(
        "/api/v1/sensor-readings",
        headers=headers,
        json=payload,
    )

    second_response = client.post(
        "/api/v1/sensor-readings",
        headers=headers,
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Duplicate device event."
    }


def test_sensor_ingestion_rejects_sensor_identity_mismatch(
    client,
    provisioned_test_sensor,
):
    sensor, raw_api_key = provisioned_test_sensor

    response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": sensor.public_id,
            "X-Device-API-Key": raw_api_key,
        },
        json={
            "device_event_id": "pytest-mismatch-event-001",
            "sensor_public_id": "00000000-0000-0000-0000-000000000000",
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Authenticated sensor does not match payload sensor."
    }


def test_sensor_ingestion_rejects_wrong_key_for_existing_sensor(
    client,
    provisioned_test_sensor,
):
    sensor, _ = provisioned_test_sensor

    response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": sensor.public_id,
            "X-Device-API-Key": "wrong-device-api-key",
        },
        json={
            "device_event_id": "pytest-wrong-key-event-001",
            "sensor_public_id": sensor.public_id,
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid device credentials."
    }


def test_sensor_ingestion_rejects_future_recorded_at(
    client,
    provisioned_test_sensor,
):
    from datetime import timedelta

    sensor, raw_api_key = provisioned_test_sensor

    response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": sensor.public_id,
            "X-Device-API-Key": raw_api_key,
        },
        json={
            "device_event_id": "pytest-future-time-event-001",
            "sensor_public_id": sensor.public_id,
            "temperature_c": 20.0,
            "recorded_at": (
                datetime.now(timezone.utc) + timedelta(minutes=10)
            ).isoformat(),
        },
    )

    assert response.status_code == 422


def test_sensor_device_key_rotation_invalidates_old_key(
    client,
    db_session,
    provisioned_test_sensor,
):
    from backend.app.services.sensor_service import (
        rotate_sensor_device_api_key,
    )

    sensor, old_api_key = provisioned_test_sensor

    new_api_key = rotate_sensor_device_api_key(
        db=db_session,
        sensor=sensor,
    )

    old_key_response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": sensor.public_id,
            "X-Device-API-Key": old_api_key,
        },
        json={
            "device_event_id": "pytest-old-key-event-001",
            "sensor_public_id": sensor.public_id,
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    new_key_response = client.post(
        "/api/v1/sensor-readings",
        headers={
            "X-Sensor-ID": sensor.public_id,
            "X-Device-API-Key": new_api_key,
        },
        json={
            "device_event_id": "pytest-new-key-event-001",
            "sensor_public_id": sensor.public_id,
            "temperature_c": 20.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert old_key_response.status_code == 401
    assert new_key_response.status_code == 201


def test_admin_can_register_sensor_and_receive_one_time_device_key(
    client,
    admin_auth_headers,
):
    response = client.post(
        "/api/v1/sensors",
        headers=admin_auth_headers,
        json={
            "sensor_code": "PYTEST-REGISTER-001",
            "name": "Pytest Registration Sensor",
            "sensor_type": "temperature",
            "latitude": 27.0,
            "longitude": 88.0,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["sensor_code"] == "PYTEST-REGISTER-001"
    assert body["device_api_key"]
    assert len(body["device_api_key"]) >= 32


def test_get_sensor_does_not_expose_device_api_key(
    client,
    admin_auth_headers,
    provisioned_test_sensor,
):
    sensor, _ = provisioned_test_sensor

    response = client.get(
        f"/api/v1/sensors/{sensor.public_id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["public_id"] == sensor.public_id
    assert "device_api_key" not in body


def test_admin_can_rotate_sensor_device_key_via_api(
    client,
    admin_auth_headers,
    provisioned_test_sensor,
):
    sensor, old_api_key = provisioned_test_sensor

    response = client.post(
        f"/api/v1/sensors/{sensor.public_id}/rotate-device-key",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["public_id"] == sensor.public_id
    assert body["device_api_key"]
    assert body["device_api_key"] != old_api_key
    assert len(body["device_api_key"]) >= 32
