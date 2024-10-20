import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def get_engine(db_path='sqlite:///data/portfolios.db'):
    # Extract the directory path from db_path
    db_dir = os.path.dirname(db_path.replace('sqlite:///', '', 1))

    # Create the directory if it doesn't exist
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()