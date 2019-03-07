from flask import Blueprint, request, jsonify
import json

from app.models.User import User
from app.jwt import encode

authentication = Blueprint('authentication', __name__)

@authentication.route('/api/login', methods=['GET'])
def login():
    """User login function"""
    # request_data = request.get_data()
    # data = json.loads(request_data)
    User.get_user_by_id("trachpro@gmail.com")
    # print("data: ", data)
    return jsonify({"vasf: ""asfd"}), 200
    # if

@authentication.route('/api/admin_login', methods=['POST'])
def adminLogin():
    """Admin login"""
    request_data = request.get_data()
    data = json.loads(request_data)

    if data and data['username'] and data['password']:
        if data['username'] == 'admin' and data['password']=='123456':
            return jsonify({
                "jwt": encode({"id": -1})
            }), 200

    return jsonify({
        "status": 0,
        "message": "username or password is incorrect"
    }), 400