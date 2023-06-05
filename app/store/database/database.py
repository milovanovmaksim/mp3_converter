from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.engine.url import URL

from app.store.database import db

if TYPE_CHECKING:
    from aiohttp.web import Application
    from app.store.database.config import DatabaseConfig


class Database:
    """
    Класс для соединения с базой данных.
    """
    def __init__(self, config: "DatabaseConfig"):
        self.config = config
        self._engine: Optional[AsyncEngine]
        self._db: Any
        self.session: async_sessionmaker[AsyncSession]

    async def connect(self, _: "Application") -> None:
        """
        Создает объект класса AsyncSession. Метод вызывается один раз при запуске приложения.
        """
        self._db = db
        self._engine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                host=self.config.host,
                database=self.config.database,
                username=self.config.user,
                password=self.config.password,
                port=self.config.port,
                ),
            echo=False,
            future=True
        )
        self.session = async_sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)

    async def disconnect(self, _: "Application") -> None:
        """
        Удаляет пул соединений, используемый текущей сессией self.session.
        Метод вызывается один раз при остановке приложения.
        """
       
        if self._engine:
            await self._engine.dispose()
