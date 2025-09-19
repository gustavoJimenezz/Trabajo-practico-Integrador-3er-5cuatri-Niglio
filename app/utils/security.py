# Decorador para validar rol del usuario
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("rol") != role:
                return jsonify(msg="Acceso denegado, rol incorrecto"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator