from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///blog.db", connect_args={"check_same_thread": False})

LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
