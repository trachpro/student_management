from sqlalchemy import Column, Integer, ForeignKey
from marshmallow import Schema, fields, validate, pre_load

from database import Base, db_session as session

# from app.models.Class import Class

class Enroll(Base):
    __tablename__ = 'enrolls'

    user_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
    status = Column(Integer, nullable=False, default=1)

    def __init__(self, user_id, class_id, status):
        self.user_id = user_id
        self.class_id = class_id
        self.status = status

    @classmethod
    def get_enroll_by_user_id(cls, user_id):
        return session.query(Enroll).filter_by(user_id=user_id)

    @classmethod
    def get_enroll_by_class_id(cls, class_id):
        return session.query(Enroll).filter_by(class_id=class_id)

    @classmethod
    def get_enroll_by_class_id_and_user_id(cls, class_id, user_id):
        return session.query(Enroll).filter_by(class_id=class_id, user_id = user_id).first()

    @classmethod
    def register_new_enroll(cls, user_id, class_id):
        user = Enroll(user_id=user_id, class_id=class_id, status=1)
        return user
    
    

class EnrollSchema(Schema):

    user_id = fields.Int(required=True)
    class_id = fields.Int(required=True)
    status = fields.Int()