from sqlalchemy import Column, Integer, String
from marshmallow import Schema, fields, validate, pre_load
from marshmallow.validate import Range

from app.models.Enroll import Enroll
from database import Base, db_session as session

class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    student_limit = Column(Integer, nullable=False)
    current_student = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=1)
    tutor_id = Column(Integer, nullable=False)

    def __init__(self, name, student_limit, current_student, status, tutor_id):
        self.name = name
        self.student_limit = student_limit
        self.current_student = current_student
        self.status = status,
        self.tutor_id = tutor_id

    @classmethod
    def get_class_by_tutor_id(cls, tutor_id):
        return session.query(Class).filter_by(tutor_id=tutor_id)

    @classmethod
    def get_all_class(cls):
        return session.query(Class).all()

    @classmethod
    def get_class_by_id(cls, class_id):
        return session.query(Class).filter_by(id=class_id).first()

    @classmethod
    def register_new_class(cls, name, student_limit, tutor_id):
        data = Class(name=name, student_limit=student_limit, tutor_id=tutor_id, current_student = 0,status = 1)
        return data
    
    @classmethod
    def get_my_class_student(cls, user_id):
        return session.query(Class).filter_by(status=1).join(Enroll).filter_by(user_id = user_id, status=1)

    @classmethod
    def get_my_class_tutor(cls, tutor_id):
        return session.query(Class).filter_by(tutor_id=tutor_id, status=1).all()


class ClassSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, error="User's name cannot be empty"),
            validate.Length(max=50, error="User's name is limited to 100 characters")
        ]
    )

    student_limit = fields.Int(
        required=True,
        validate=[
            Range(min=1, max=15, error="the number of student must be between 1 and 15")
        ]
    )

    tutor_id = fields.Int(required=True)
    status = fields.Int()
    current_student = fields.Int()
