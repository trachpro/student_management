from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'mysql+pymysql://root:hamphuong3003@localhost:3306/student_management'

engine = create_engine(DATABASE_URI)
Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))