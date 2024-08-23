import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DEBUG

load_dotenv()

username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
database = os.getenv('DATABASE')
test_database = os.getenv('TEST_DATABASE')

if DEBUG:
    DATABASE_URL = f'postgresql://{username}:{password}@localhost:5432/{test_database}'
else:
    DATABASE_URL = f'postgresql://{username}:{password}@localhost:5432/{database}'


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)