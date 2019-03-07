from sqlalchemy import Column, Integer, String
from marshmallow import Schema, fields, validate, pre_load

from database import Base, db_session as session

class User(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(20), nullable=False, unique=True)
    role = Column(Integer, nullable=False)

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

    @classmethod
    def get_user_by_id(cls, email):
        return session.query(User).filter_by(email=email).first()

    @classmethod
    def register_new_user(cls, name, email, role):
        user = User(name=name, email=email, role=role)
        return user

class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, error="User's name cannot be empty"),
            validate.Length(max=100, error="User's name is limited to 100 characters")
        ]
    )

    email = fields.Email(required=True)

    @pre_load()
    def trim_spaces(selfs, data):
        if isinstance(data['name'], str):
            data['name'] = data['name'].strip()

        return data