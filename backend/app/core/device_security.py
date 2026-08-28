import hashlib
import hmac
import secrets


def generate_device_api_key() -> str:
    return secrets.token_urlsafe(32)


def hash_device_api_key(api_key: str) -> str:
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def verify_device_api_key(
    api_key: str,
    api_key_hash: str,
) -> bool:
    candidate_hash = hash_device_api_key(api_key)

    return hmac.compare_digest(
        candidate_hash,
        api_key_hash,
    )
