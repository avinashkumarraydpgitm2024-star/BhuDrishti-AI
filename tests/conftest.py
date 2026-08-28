import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import backend.app.models  # noqa: F401
from backend.app.core.database import Base, get_db
from backend.app.main import app


TEST_DATABASE_URL = "sqlite:///./test_bhudrishti.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

from backend.app.core.device_security import hash_device_api_key
from backend.app.models.sensor import Sensor, SensorType


@pytest.fixture
def provisioned_test_sensor(db_session):
    raw_api_key = "pytest-device-api-key-1234567890"

    sensor = Sensor(
        sensor_code="PYTEST-SENSOR-001",
        name="Pytest Sensor",
        sensor_type=SensorType.TEMPERATURE,
        latitude=27.0,
        longitude=88.0,
        device_api_key_hash=hash_device_api_key(raw_api_key),
    )

    db_session.add(sensor)
    db_session.commit()
    db_session.refresh(sensor)

    return sensor, raw_api_key



from backend.app.core.security import create_access_token, hash_password
from backend.app.models.user import User, UserRole


@pytest.fixture
def admin_auth_headers(db_session):
    user = User(
        full_name="Pytest Admin",
        email="pytest-admin@example.com",
        password_hash=hash_password("pytest-admin-password"),
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    access_token = create_access_token(
        subject=user.public_id,
    )

    return {
        "Authorization": f"Bearer {access_token}"
    }
