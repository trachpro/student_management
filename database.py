from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'mysql+pymysql://u5x7vnoqw4vzp6fd:N2WzfPgDZM9ugeKof3hs@bysavq0fwvmxkhrrkq4j-mysql.services.clever-cloud.com:3306/bysavq0fwvmxkhrrkq4j'

engine = create_engine(DATABASE_URI)
Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))