Давайте создадим проект с необходимой структурой и кодом, соответствующим вашему запросу по созданию моделей User и Task, их связям, а также коду для файла main.py. Также я укажу, как запускать проект из командной строки.

1. Структура проекта
Проект будет иметь следующую структуру:

project/
│
├── app/
│   ├── backend/
│   │   └── db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── user.py
│   └── routers/
│       ├── __init__.py
│       ├── main.py
│       └── schemas.py
└── requirements.txt
2. Установка библиотек
Создайте файл requirements.txt в корневой директории проекта
pip freeze > requirements.txt

и добавьте следующую строку:

sqlalchemy
fastapi
uvicorn
Затем выполните команду в терминале, чтобы установить все зависимости:

pip install -r requirements.txt
3. Код для файла db.py
В файле db.py в директории backend должен быть следующий код:

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

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Печатаем SQL запросы на создание таблиц
from sqlalchemy.schema import CreateTable

print(CreateTable(User.__table__).compile(engine))
print(CreateTable(Task.__table__).compile(engine))
4. Код для модели User в user.py
В файле user.py в директории models добавьте следующий код:

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    # Связь с задачами
    tasks = relationship("Task", back_populates='user')
5. Код для модели Task в task.py
В файле task.py в директории models должен быть следующий код:

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    # Связь с пользователем
    user = relationship("User", back_populates='tasks')
6. Обновление __init__.py в директории models
В файле __init__.py в директории models добавьте следующее:

from .user import User
from .task import Task
7. Код для файла main.py
Теперь создайте файл main.py в директории routers с содержимым:

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.backend.db import SessionLocal, engine
from app.models import Base, User, Task
from pydantic import BaseModel
from typing import List

# Создаем базу данных (если еще не создана)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Модель Pydantic для создания пользователя
class UserCreate(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

# Модель Pydantic для создания задачи
class TaskCreate(BaseModel):
    title: str
    content: str
    priority: int = 0
    completed: bool = False
    user_id: int
    slug: str

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Конечная точка для создания пользователя
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Конечная точка для получения всех пользователей
@app.get("/users/", response_model=List[UserCreate])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Конечная точка для создания задачи
@app.post("/tasks/", response_model=TaskCreate)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Конечная точка для получения всех задач
@app.get("/tasks/", response_model=List[TaskCreate])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks
8. Запуск проекта
Теперь, чтобы запустить ваше приложение, выполните следующую команду из корневой директории проекта:

uvicorn app.routers.main:app --reload
Параметр --reload автоматически перезагрузит сервер при внесении изменений в код.