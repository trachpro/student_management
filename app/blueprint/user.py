from flask import Blueprint, request, jsonify
from app.models.User import UserSchema, User
from app.models.Class import Class
from app.utils.validation import validate_schema, access_token_required, get_value_from_access_token, is_valid_password
from database import db_session as session
from passlib.hash import sha256_crypt
from app.utils.error import Error, StatusCode
from sqlalchemy.exc import IntegrityError

user = Blueprint('user', __name__)


@user.route('/api/users', methods=['POST'])
# @access_token_required
def create_user():
    role = get_value_from_access_token()
    print("role: ", role)
    data = dict()
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({
            "status": 0,
            "message": "invalid format json type"
        }), 400
    
    schema = UserSchema()
    result = validate_schema(schema, data)

    if bool(result.errors):
        result.errors['status'] = 0
        return jsonify(result.errors), 400

    if data['role'] == 2 and role != 1:
        return jsonify({
            "status": 0,
            "message": "You have to be admin to create Tutor account!"
        }), 403
    elif  data['role'] != 2 and data['role'] !=3:
        return jsonify({
            "status": 0,
            "message": "Invalid role"
        }), 400

    if data['role'] == 2:
        data['password'] = sha256_crypt.encrypt("123456")
    else:
        if data.get('password') and is_valid_password(data.get('password')):
            print("password: ", data['password'])
            data['password'] = sha256_crypt.encrypt(data.get('password'))
        else:
            return jsonify({
                "status": 0,
                "message": "the password have to be from 5 to 10 characters, no space and has at least one number"
            }), 400

    newUser = User.register_new_user(data['name'], data['email'], data['role'], data['password'])

    try:
        session.add(newUser)
        session.commit()
        pass
    except IntegrityError as e:
        return jsonify({
            "status": 0,
            "message": "Email is in used!"
        }), 400
    

    return jsonify({
        'status': 1,
        'message': "new User created",
        'data': schema.dump(newUser)
    }), 200


@user.route('/api/student-classes/<int:class_id>', methods=['GET'])
@access_token_required
def get_student_class(class_id, *args, **kwargs):

    schema = UserSchema(many=True)

    target_class = Class.get_class_by_id(class_id)

    if not bool(target_class):
        return jsonify({
            "status": 0,
            "message": "class not found!"
        }), 400

    if target_class.tutor_id != kwargs['user_id']:
        return jsonify({
            "status": 0,
            "message": "you are not allowed to get student of this class!"
        }), 400

    result = User.get_student_class_tutor(class_id)

    return jsonify({
        "data": schema.dump(result),
        "status": 1
    })