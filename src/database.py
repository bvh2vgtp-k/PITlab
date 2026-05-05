from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, echo=True)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    """подключегние к базе"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_db_and_tables():
    """Создает все таблицы в базе данных"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Возвращает сессию для работы с базой данных"""
    with Session(engine) as session:
        yield session