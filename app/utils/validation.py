import datetime
from functools import wraps

import jwt
from flask import request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from marshmallow import ValidationError

from app.utils.error import Error, StatusCode

SECRET_KEY = "my secret key"

def access_token_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            errors = {
                "token": "Access token was missing"
            }
            raise Error(StatusCode.UNAUTHORIZED, "Missing authorization header", errors)

        token = auth_header.split(" ")[1]

        if not token:
            errors = {
                "token": "Access token was missing"
            }
            raise Error(StatusCode.UNAUTHORIZED, "Unauthorized request", errors)

        try:
            # Decode token by app's secret key
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # Check that token is expired
            errors = {
                "token": "Token has expired. Please login again"
            }
            raise Error(StatusCode.UNAUTHORIZED, "Your session has expired. Please login again", errors)

        except jwt.InvalidTokenError:
            # Check that token is invalid
            errors = {
                "token": "Invalid token"
            }
            raise Error(StatusCode.UNAUTHORIZED, "Request unauthorized", errors)

        id = payload['id']
        return f(id=id, *args, **kwargs)

    return decorated_func


def validate_schema(schema, data):
    """Validate request data
    Return a tuple (success, data)
    success: True if passing validation
    data: if success is False, data is set to error messages, else set to validated data
    """
    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        errors = e.messages
        raise Error(StatusCode.BAD_REQUEST, "Validation failed", errors)

    return validated_data


def jwt_encode(user):
    token = jwt.encode({
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }, SECRET_KEY)
    return token


def jwt_decode(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
