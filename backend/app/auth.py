import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
    return f"pbkdf2_sha256${salt}${base64.b64encode(digest).decode()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, salt, stored = encoded.split("$", 2)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
        return hmac.compare_digest(base64.b64encode(digest).decode(), stored)
    except (TypeError, ValueError):
        return False


def secret_key() -> str:
    secret = os.getenv("AUTH_SECRET")
    if secret:
        if len(secret) < 32:
            raise RuntimeError("AUTH_SECRET must contain at least 32 characters")
        return secret
    if os.getenv("APP_ENV", "development").lower() == "production":
        raise RuntimeError("AUTH_SECRET is required when APP_ENV=production")
    return "development-only-feedz-secret-change-me"


def create_session(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "86400")),
    }
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    signature = hmac.new(secret_key().encode(), body.encode(), hashlib.sha256).digest()
    return f"{body}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"


def verify_session(token: str) -> Optional[Dict]:
    try:
        body, signature = token.split(".", 1)
        padded_signature = signature + "=" * (-len(signature) % 4)
        supplied = base64.urlsafe_b64decode(padded_signature.encode())
        expected = hmac.new(secret_key().encode(), body.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(supplied, expected):
            return None
        padded_body = body + "=" * (-len(body) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded_body.encode()))
        if payload["exp"] < int(time.time()):
            return None
        return payload
    except (ValueError, KeyError, json.JSONDecodeError):
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    payload = verify_session(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
    return {"id": payload["sub"]}
