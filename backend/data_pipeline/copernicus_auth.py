import os

from dotenv import load_dotenv


load_dotenv()


def get_copernicus_credentials():
    username = os.getenv("COPERNICUS_USERNAME")
    password = os.getenv("COPERNICUS_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Copernicus credentials are missing from .env"
        )

    return {
        "username": username,
        "password": password
    }
