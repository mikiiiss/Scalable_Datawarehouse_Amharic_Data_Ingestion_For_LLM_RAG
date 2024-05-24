from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os,sys

from dotenv import load_dotenv

load_dotenv()
rpath = os.path.abspath('../api')
SQLALCHEMY_DATABASE_URL = os.getenv('DB_CONNECTION_STRING')


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

def get_base():
        return Base

 
