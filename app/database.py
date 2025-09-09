from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# "postgresql+psycopg2://<username>:<password>@<ip-address>/<database>"
DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost/fastapi"

engine = create_engine(DATABASE_URL)
# create session to talk to database
session_local = sessionmaker(autocommit = False, autoflush=False, bind=engine)
# all models & tables that we create will be extending this Base class
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()