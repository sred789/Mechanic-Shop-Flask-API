from datetime import datetime, timedelta
from jose import jwt
from flask import current_app

def encode_token(customer_id: int) -> str:
    payload = {
        "customer_id": customer_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.JWTError:
        return {"error": "Invalid token"}