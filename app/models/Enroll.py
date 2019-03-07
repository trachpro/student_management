from sqlalchemy import Column, Integer, ForeignKey

from database import Base, db_session as session

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
    def get_enroll_by_class_id(cls, user_id):
        return session.query(Enroll).filter_by(user_id=user_id)

    @classmethod
    def register_new_enroll(cls, user_id, class_id):
        user = Enroll(user_id=user_id, class_id=class_id)
        return user

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