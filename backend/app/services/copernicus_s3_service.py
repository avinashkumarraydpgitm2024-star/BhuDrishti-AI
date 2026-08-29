from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import boto3

from backend.app.core.config import settings


def create_cdse_s3_client():
    if not settings.cdse_access_key or not settings.cdse_secret_key:
        raise RuntimeError(
            "CDSE S3 credentials are not configured."
        )

    return boto3.client(
        "s3",
        endpoint_url=settings.cdse_s3_endpoint,
        aws_access_key_id=settings.cdse_access_key,
        aws_secret_access_key=settings.cdse_secret_key,
        region_name=settings.cdse_s3_region,
    )


def parse_cdse_s3_url(
    s3_url: str,
) -> tuple[str, str]:
    parsed = urlparse(s3_url.strip())

    if parsed.scheme != "s3":
        raise ValueError(
            "Expected an S3 satellite asset URL."
        )

    if parsed.netloc != "eodata":
        raise ValueError(
            "Only the Copernicus eodata bucket is supported."
        )

    key = parsed.path.lstrip("/")

    if not key:
        raise ValueError(
            "S3 asset URL does not contain an object key."
        )

    return parsed.netloc, key


def download_cdse_s3_asset(
    *,
    s3_url: str,
    destination: str | Path,
) -> Path:
    bucket, key = parse_cdse_s3_url(s3_url)

    destination_path = Path(destination)
    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    client = create_cdse_s3_client()

    client.download_file(
        bucket,
        key,
        str(destination_path),
    )

    return destination_path
