# import os

from flask import Flask, jsonify

from app.blueprint.authentication import authentication
from app.blueprint.user import user, UserSchema
from app.blueprint.classes import classes
from app.blueprint.enroll import enroll
from app.utils.error import Error
from database import db_session as session

print("name: ", __name__)
app = Flask(__name__)
app.register_blueprint(authentication)
app.register_blueprint(user)
app.register_blueprint(classes)
app.register_blueprint(enroll)

@app.teardown_appcontext
def close_db_session(exception):
    """Remove database session on request ends"""
    session.remove()


@app.errorhandler(404)
def handle_not_found(exception):
    """Handle an invalid endpoint"""
    return jsonify({
        'message': 'Resource not found'
    }), 404


@app.errorhandler(Error)
def handle_exception(error):
    return error.to_response()


@app.errorhandler(500)
def handle_internal_error(exception):
    """Rollback database transaction if any error occurs"""
    logging.error(exception)
    session.rollback()
    return jsonify({
        'message': 'An unexpected internal error has occurred'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
