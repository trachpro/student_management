from flask import Blueprint, request, jsonify
from app.models.Class import ClassSchema, Class
from app.models.User import UserSchema
from app.models.Enroll import EnrollSchema, Enroll
from app.utils.validation import validate_schema, access_token_required, get_value_from_access_token, is_valid_password
from database import db_session as session
from app.utils.error import Error, StatusCode
from sqlalchemy.exc import IntegrityError

enroll = Blueprint('enroll', __name__)


@enroll.route('/api/enrolls/<int:class_id>', methods=['POST'])
@access_token_required
def join_class(class_id,*args, **kwargs):
    role = kwargs['role']
    
    if role != 3:
        return jsonify({
            "status": 0,
            "message": "Only student can join class!"
        }), 400
        
    schema = EnrollSchema()

    target_enroll = Enroll.get_enroll_by_class_id_and_user_id(class_id, kwargs['user_id'])

    if bool(target_enroll):
        message = "you are already in this class"

        if not target_enroll.status:
            message = "you are deleted from this class"
        return jsonify({
            "status": 0,
            "message": message
        }), 400

    target_class = Class.get_class_by_id(class_id)

    if not bool(target_class):
        return jsonify({
            "status": 0,
            "message": "class not found!"
        }), 400

    if not target_class.status:
        return jsonify({
            "status": 0,
            "message": "class is already deleted!"
        }), 400

    if target_class.student_limit <= target_class.current_student:
        return jsonify({
            "status": 0,
            "message": "this class is full!"
        }), 400

    new_enroll  = Enroll.register_new_enroll(kwargs['user_id'], class_id)

    try:
        session.add(new_enroll)
        target_class.current_student += 1
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
        'data': schema.dump(new_enroll)
    }), 200


@enroll.route('/api/enrolls/<int:class_id>', methods=['DELETE'])
@access_token_required
def cancel_class(class_id,*args, **kwargs):
    role = kwargs['role']
    
    if role != 3 and role != 2:
        return jsonify({
            "status": 0,
            "message": "you are not allowed to cancel class"
        }), 400
        
    schema = EnrollSchema()

    target_enroll = Enroll.get_enroll_by_class_id_and_user_id(class_id, kwargs['user_id'])

    if bool(target_enroll):

        if not target_enroll.status:
            return jsonify({
                "status": 0,
                "message": "you are deleted from this class"
            }), 400
    else:
        return jsonify({
            "status": 0,
            "message": "enroll not found!"
        }), 400
    
    target_class = Class.get_class_by_id(class_id)

    if (kwargs['role'] == 2 and kwargs['user_id'] != target_class.tutor_id) or (kwargs['user_id'] != target_enroll.user_id) :
        return jsonify({
            "status": 0,
            "message": "you are not allow to delete this enroll!"
        }), 400

    try:
        target_enroll.status = 0
        target_class.current_student -= 1
        session.commit()
        pass
    except IntegrityError as e:
        return jsonify({
            "status": 0,
            "message": "deleted error!"
        }), 400
    

    return jsonify({
        'status': 1,
        'message': "deleted!",
        'data': schema.dump(target_enroll)
    }), 200