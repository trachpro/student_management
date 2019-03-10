from flask import Blueprint, request, jsonify
import json

from app.models.User import User
from app.utils.jwt import encode
from passlib.hash import sha256_crypt

authentication = Blueprint('authentication', __name__)


@authentication.route('/api/login', methods=['POST'])
def login():
    """User login function"""
    data = dict()
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({
            "status": 0,
            "message": "invalid format json type"
        }), 400

    if not data or not data.get('password') or not data.get('email'):
        return jsonify({
            "status": 0,
            "message": "email and password is required!"
        }), 401

    user = User.get_user_by_id(data['email'])

    if user and sha256_crypt.verify(data['password'], user.password):
        return jsonify({
            "jwt": encode({"id": user.id, 'role': user.role}),
            "status": 1
        }), 401
    else:
        return jsonify({
            "status": 0,
            "message": "email or password is incorrect!"
        }), 40


@authentication.route('/api/admin_login', methods=['POST'])
def admin_login():
    """Admin login"""
    data = dict()
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({
            "status": 0,
            "message": "invalid format json type"
        }), 400

    if data and data.get('username') and data.get('password'):
        if data['username'] == 'admin' and data['password'] == '123456':
            return jsonify({
                "jwt": encode({"id": -1, 'role': 1})
            }), 200

    return jsonify({
        "status": 0,
        "message": "username or password is incorrect"
    }), 400
