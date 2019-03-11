from flask import Blueprint, request, jsonify
from app.models.Class import ClassSchema, Class
from app.utils.validation import validate_schema, access_token_required, get_value_from_access_token, is_valid_password
from database import db_session as session
from app.utils.error import Error, StatusCode
from sqlalchemy.exc import IntegrityError

classes = Blueprint('class', __name__)


@classes.route('/api/classes', methods=['POST'])
@access_token_required
def create_class(*args, **kwargs):
    role = kwargs['role']

    data = dict()
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({
            "status": 0,
            "message": "invalid format json type"
        }), 400
    
    if role != 2:
        return jsonify({
            "status": 0,
            "message": "Only teacher can create class!"
        }), 400
    data['tutor_id'] = kwargs['user_id']
    schema = ClassSchema()
    result = validate_schema(schema, data)
    
    if bool(result.errors):
        result.errors['status'] = 0
        return jsonify(result.errors), 400

    new_class = Class.register_new_class(data['name'], data['student_limit'], data['tutor_id'])

    try:
        session.add(new_class)
        session.commit()
        pass
    except IntegrityError as e:
        return jsonify({
            "status": 0,
            "message": "cannot create class!"
        }), 400
    

    return jsonify({
        'status': 1,
        'message': "new Class created",
        'data': schema.dump(new_class)
    }), 200

@classes.route('/api/classes/<int:class_id>', methods=['PUT'])
@access_token_required
def update_class(class_id,*args, **kwargs):
    # class_id = 1
    print(id, class_id, kwargs['role'])
    role = kwargs['role']

    data = dict()
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({
            "status": 0,
            "message": "invalid format json type"
        }), 400
    
    if role != 2:
        return jsonify({
            "status": 0,
            "message": "Only teacher can update class!"
        }), 400
    data['tutor_id'] = kwargs['user_id']

    rawClass = Class.get_class_by_id(class_id)

    if not bool(rawClass):
        return jsonify({
            "status": 0,
            "message": "class not found!"
        }), 400

    if not rawClass.status:
        return jsonify({
            "status": 0,
            "message": "this class is already deleted!"
        }), 400

    if kwargs['user_id'] != rawClass.tutor_id:
        return jsonify({
            "status": 0,
            "message": "you are not allowed to update this class!"
        }), 403

    schema = ClassSchema()
    result = validate_schema(schema, data)
    
    if data.get('name'):
        if not result.errors.get('name'):
            rawClass.name = data.get('name')
        else:
            return jsonify({
                "status": 0,
                "message": "invalid class name!"
            }), 400
    
    if data.get('student_limit'):
        if not result.errors.get('student_limit') and data.get('student_limit') >= rawClass.current_student:
            rawClass.student_limit = data.get('student_limit')
        else:
            return jsonify({
                "status": 0,
                "message": "student limit must be greater than number of current student!"
            }), 400


    try:
        session.commit()
        pass
    except IntegrityError as e:
        return jsonify({
            "status": 0,
            "message": "cannot update class!"
        }), 400

    return jsonify({
        "data": schema.dump(rawClass)
    }), 200


@classes.route('/api/classes/<int:class_id>', methods=['DELETE'])
@access_token_required
def delete_class(class_id,*args, **kwargs):
    rawClass = Class.get_class_by_id(class_id)

    if not bool(rawClass):
        return jsonify({
            "status": 0,
            "message": "class not found!"
        }), 400

    if not rawClass.status:
        return jsonify({
            "status": 0,
            "message": "this class is already deleted!"
        }), 400

    if kwargs['user_id'] != rawClass.tutor_id:
        return jsonify({
            "status": 0,
            "message": "you are not allowed to delete this class!"
        }), 403

    rawClass.status = 0

    try:
        # session.update(rawClass)
        session.commit()
        pass
    except IntegrityError as e:
        return jsonify({
            "status": 0,
            "message": "cannot update class!"
        }), 400

    schema = ClassSchema()

    return jsonify({
        "status": 1,
        "message": "class is deleted!",
        "data": schema.dump(rawClass)
    }), 200

@classes.route('/api/classes', methods=['GET'])
def get_all():
    schema = ClassSchema(many=True)

    data = Class.get_all_class()

    return jsonify({
        "data": schema.dump(data),
        "status": 1
    })


@classes.route('/api/my-classes', methods=['GET'])
@access_token_required
def get_my_class(*args, **kwargs):

    schema = ClassSchema(many=True)

    result = Class.get_my_class_student(kwargs['user_id'])

    return jsonify({
        "data": schema.dump(result),
        "status": 1
    })

@classes.route('/api/tutor-classes', methods=['GET'])
@access_token_required
def get_tutor_class(*args, **kwargs):

    schema = ClassSchema(many=True)

    result = Class.get_my_class_tutor(kwargs['user_id'])

    return jsonify({
        "data": schema.dump(result),
        "status": 1
    })
