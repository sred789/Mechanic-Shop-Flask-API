# from datetime import datetime, timedelta
# from jose import jwt
# from flask import current_app

# def encode_token(customer_id: int) -> str:
#     payload = {
#         "customer_id": customer_id,
#         "exp": datetime.utcnow() + timedelta(hours=24)
#     }
#     return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

# def decode_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
#         return payload
#     except jwt.ExpiredSignatureError:
#         return {"error": "Token expired"}
#     except jwt.JWTError:
#         return {"error": "Invalid token"}

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from flask import current_app


def encode_token(customer_id: int) -> str:
    """
    Returns a JWT for a customer.
    """
    payload = {
        "customer_id": customer_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }

    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not set in app config")

    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str) -> dict:
    """
    Returns decoded payload or raises JWTError if invalid/expired.
    """
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not set in app config")

    # jose will raise JWTError (including expired)
    return jwt.decode(token, secret, algorithms=["HS256"])