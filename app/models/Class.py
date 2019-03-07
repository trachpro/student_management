from sqlalchemy import Column, Integer, String
# from marshmallow import Schema, fields, validate, pre_load

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

    # @classmethod
    # def get_class_by_tutor_id(cls, tutor_id):
    #     return session.query(Class).filter_by(tutor_id=tutor_id)

    # @classmethod
    # def get_class_by_id(cls, class_id):
    #     return session.query(Class).filter_by(id=class_id)

    # @classmethod
    # def register_new_class(cls, name, student_limit, tutor_id):
    #     data = Class(name=name, student_limit=student_limit, tutor_id=tutor_id)
    #     return data

# class UserSchema(Schema):
#     id = fields.Int()
#     name = fields.Str(
#         required=True,
#         validate=[
#             validate.Length(min=1, error="User's name cannot be empty"),
#             validate.Length(max=100, error="User's name is limited to 100 characters")
#         ]
#     )
#
#     email = fields.Email(required=True)
#
#     @pre_load()
#     def trim_spaces(selfs, data):
#         if isinstance(data['name'], str):
#             data['name'] = data['name'].strip()
#
#         return data