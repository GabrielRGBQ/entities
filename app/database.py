from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: This is a bad practice. Should be done using env variables.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Pucela.23@localhost/fastapi"
# url format: "postgresql://<username>:<password>@<ipaddress/hostname>/<database_name>""

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
