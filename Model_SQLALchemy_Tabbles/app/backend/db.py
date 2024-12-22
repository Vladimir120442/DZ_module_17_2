from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем движок базы данных
DATABASE_URL = 'sqlite:///taskmanager.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем локальную сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Импортируем модели
from app.models import User, Task

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Печатаем SQL-запросы на создание таблиц
from sqlalchemy.schema import CreateTable

print(CreateTable(User.__table__).compile(engine))
print(CreateTable(Task.__table__).compile(engine))