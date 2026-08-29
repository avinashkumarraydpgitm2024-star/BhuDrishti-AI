from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import requests


DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_MAX_BYTES = 250 * 1024 * 1024


def download_https_asset(
    *,
    url: str,
    destination: str | Path,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> Path:
    parsed = urlparse(url.strip())

    if parsed.scheme != "https":
        raise ValueError(
            "Only HTTPS satellite assets are supported by this downloader."
        )

    if not parsed.netloc:
        raise ValueError("Satellite asset URL is invalid.")

    destination_path = Path(destination)
    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = destination_path.with_suffix(
        destination_path.suffix + ".part"
    )

    total_bytes = 0

    try:
        with requests.get(
            url,
            stream=True,
            timeout=timeout_seconds,
        ) as response:
            response.raise_for_status()

            content_length = response.headers.get(
                "Content-Length"
            )

            if content_length is not None:
                declared_size = int(content_length)

                if declared_size > max_bytes:
                    raise ValueError(
                        "Satellite asset exceeds the configured size limit."
                    )

            with temporary_path.open("wb") as output:
                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):
                    if not chunk:
                        continue

                    total_bytes += len(chunk)

                    if total_bytes > max_bytes:
                        raise ValueError(
                            "Satellite asset exceeds the configured size limit."
                        )

                    output.write(chunk)

        temporary_path.replace(destination_path)

    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()

        raise

    return destination_path


def validate_download_destination(
    destination: str | Path,
) -> Path:
    path = Path(destination)

    if path.suffix.lower() not in {
        ".jp2",
        ".tif",
        ".tiff",
    }:
        raise ValueError(
            "Unsupported satellite raster format."
        )

    return path
