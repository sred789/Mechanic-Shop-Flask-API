# from functools import wraps
# from flask import request, jsonify
# from jose import JWTError
# from .token import decode_token

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get("Authorization", "")

#         if not auth_header.startswith("Bearer "):
#             return jsonify({"error": "Token required"}), 401

#         token = auth_header.split(" ", 1)[1].strip()
#         if not token:
#             return jsonify({"error": "Token required"}), 401

#         try:
#             payload = decode_token(token)
#             customer_id = payload.get("customer_id")
#             if customer_id is None:
#                 return jsonify({"error": "Invalid token payload"}), 401
#         except JWTError:
#             return jsonify({"error": "Invalid or expired token"}), 401

#         return f(customer_id, *args, **kwargs)

#     return decorated

from functools import wraps
from flask import request, jsonify
from jose import JWTError

from .token import decode_token


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        # Expect: "Bearer <token>"
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = parts[1]

        try:
            payload = decode_token(token)
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        customer_id = payload.get("customer_id")
        if not customer_id:
            return jsonify({"error": "Invalid token payload"}), 401

        # Your routes use `customer_id` as the first argument
        return fn(customer_id, *args, **kwargs)

    return wrapper