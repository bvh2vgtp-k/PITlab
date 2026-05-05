from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from database import create_db_and_tables

from api import main_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Создаем таблицы при запуске
    create_db_and_tables()
    print("Database initialized")
    yield
    # Здесь можно добавить код очистки при завершении
    print("Shutting down...")

app = FastAPI(
    title="Museum API",
    version="0.1",
    lifespan=lifespan
)

app.include_router(main_router)

#в идеале ещё сделать ответ на рут но мне западло 

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # формат: "имя_файла:переменная_app"
        #host="0.0.0.0",  # хост (для докера обязательно надо breadcast)
        #port=8000,         # порт (по умолчанию 8000)
        #reload=True,       # авто-перезагрузка при изменении кода
    )
