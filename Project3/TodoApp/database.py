from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test1234!@127.0.0.1:3306/TodoApplicationDatabase'#test1234! is the pass for mysql db
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234@localhost/TodoApplicationDatabase'#test1234 is the password
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'# you have todosapp database with 2 tables - todos and users
# Sqlalchemy can't enhance a table for us but can only create a table for us
# we can enhance a table with alembic

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})#only for sqllite3
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()