import datetime
from functools import wraps
import re

import jwt
from flask import request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from marshmallow import ValidationError
from app.utils.jwt import encode as jwt_encode, decode as jwt_decode

from app.utils.error import Error, StatusCode

SECRET_KEY = "YOUR_SECRET_STRING"

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

        print("payload: ", payload)
        # id = payload['id']
        # kwargs['user_id']=payload['id']
        # kwargs['role']=payload['role']
        return f(user_id = payload['id'],role = payload['role'], *args, **kwargs)

    return decorated_func

def get_value_from_access_token():
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        errors = {
            "token": "Access token was missing"
        }
        return None

    token = auth_header.split(" ")[1]

    if not token:
        return None

    try:
            # Decode token by app's secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
            # Check that token is expired
        return None

    return payload['role']


def validate_schema(schema, data):
    """Validate request data
    Return a tuple (success, data)
    success: True if passing validation
    data: if success is False, data is set to error messages, else set to validated data
    """
    try:
        validated_data = schema.load(data)
        print("rasing1...")
    except ValidationError as e:
        errors = e.messages
        print("rasing...")
        raise Error(StatusCode.BAD_REQUEST, "Validation failed", errors)

    return validated_data

def is_valid_password(password):

    return re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,10}$", password)

# def jwt_encode(user):
#     token = jwt.encode({
#         "sub": user.id,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
#     }, SECRET_KEY)
#     return token


# def jwt_decode(token):
#     return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
