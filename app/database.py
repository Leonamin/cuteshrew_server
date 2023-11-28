from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core import config

db_config = {
    'user': config.settings.DB_USER,
    'password': config.settings.DB_PASSWORD,
    'host': config.settings.DB_HOST,
    'port': config.settings.DB_PORT,
    'db_name': config.settings.DB_NAME,
    'charset': config.settings.DB_CHARSET,
}

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@" \
    f"{db_config['host']}:{db_config['port']
                           }/{db_config['db_name']}?charset={db_config['charset']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
