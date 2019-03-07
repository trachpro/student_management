from database import Base, engine

from app.models.User import User
from app.models.Class import Class
from app.models.Enroll import Enroll

Base.metadata.create_all(engine)