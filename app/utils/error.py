from flask import jsonify
from marshmallow import fields, Schema


class Error(Exception):
    def __init__(self, status_code, message='', errors=None, ):
        super(Error)
        self.message = message
        self.errors = errors or {}
        self.status_code = status_code

    def to_response(self):
        resp = jsonify(ErrorSchema().dump(self))
        resp.status_code = self.status_code
        return resp


class ErrorSchema(Schema):
    message = fields.String()
    errors = fields.Raw()


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
