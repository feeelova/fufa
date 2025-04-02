from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import uvicorn
from backend.models import Base

app = FastAPI()

# Подключение к базе данных SQLite (используется асинхронный драйвер aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    """Функция для создания сессии БД"""
    async with new_session() as session:
        yield session


async def init_db():
    """Функция инициализации БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Вызываем init_db при запуске сервера
@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
