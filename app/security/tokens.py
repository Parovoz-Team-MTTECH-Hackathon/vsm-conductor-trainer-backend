from datetime import datetime, timedelta, timezone
from ..config import SECRET_KEY
import jwt


def create_token(client_id: int, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(client_id),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def create_access_token(client_id: int) -> str:
    return create_token(client_id, "access", timedelta(minutes=15))


def create_refresh_token(client_id: int) -> str:
    return create_token(client_id, "refresh", timedelta(days=30))


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"],
                      options={
                          "require": ["sub", "type", "iat", "exp"],
                      })
