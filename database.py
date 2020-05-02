#-*-coding:utf8-*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

engine = create_engine("mysql://royalfamily89:password@172.17.0.3/LIBRARY", encoding='utf8', pool_recycle=280, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
