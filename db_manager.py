from flask import Flask
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api


database = dec.declarative_base()
__factory = None
DB_PATH = 'db/database.sqlite'


def db_init(db_file=DB_PATH):
    global __factory

    if __factory:
        return

    db_file = db_file.strip()
    if not db_file:
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file}?check_same_thread=False'
    print(f'Connecting to {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from .models import __all_models

    database.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
