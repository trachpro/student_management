from flask import Blueprint, request, jsonify
from app.models.User import UserSchema, User
from app.utils.validation import validate_schema, access_token_required
from database import db_session as session
from passlib.hash import sha256_crypt

user = Blueprint('user', __name__)

@user.route('/api/users', methods=['POST'])
def createUser():

    data = dict()
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({
            "status": 0,
            "message": "invalid format json type"
        }), 400
    data['password'] = sha256_crypt.encrypt("123456")
    schema = UserSchema()
    result  = validate_schema(schema, data)

    newUser = User.register_new_user(data['name'], data['email'], data['role'], data['password'])

    session.add(newUser)
    session.commit()

    return jsonify({
        'status': 1,
        'message': "new User created",
        'data': schema.dump(newUser)
    }), 200