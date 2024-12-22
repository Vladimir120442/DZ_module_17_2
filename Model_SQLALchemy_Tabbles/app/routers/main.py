# app/routers/main.py
from app.backend.db import Base, engine

# Создание таблиц в базе данных
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Созданы таблицы:")
    for table in Base.metadata.tables:
        print(table)

if __name__ == "__main__":
    create_tables()

#    python - m uvicorn main:app
