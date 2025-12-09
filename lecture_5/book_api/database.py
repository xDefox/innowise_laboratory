# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. URL подключения к БД
DATABASE_URL = "sqlite:///./book.db"

# 2. Создаю движок
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4. Базовый класс для моделей
Base = declarative_base()


# 5. Модель Book
class Book(Base):
    __tablename__ = "books"  # имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)


# 6. Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()