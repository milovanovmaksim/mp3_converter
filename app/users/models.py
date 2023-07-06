from uuid import uuid4
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Uuid,
    insert,
    select
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from app.store.database.database import Database


class UserModel(db):
    """
    Класс, отображающий пользователей в таблице "users" базы данных.

    Args:
        id: идентификатор записи в базе данных.
        uuid: UUID.
        username: имя пользователя.
        mp3_files: экземпляр класса Mp3FileModel.
    """

    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    uuid = Column(Uuid(as_uuid=True), default=uuid4)
    username = Column(String(64), nullable=False)
    mp3_files = relationship("Mp3FileModel", back_populates="user", cascade="all, delete")

    @staticmethod
    async def add_user(database: "Database", data: dict[Any, Any]) -> "UserModel":
        """
        Добавляет нового пользователя в таблицу "users" базы данных.
        Returns:
            Возвращает экземпляр класса UserModel.
        """

        query = insert(UserModel).values(**data).returning(UserModel)
        async with database.session() as session:
            result = await session.execute(query)
            await session.commit()
            user_model = result.scalar()
            return user_model

    @staticmethod
    async def get_user_id(database: "Database", user_id: int, user_uuid: str) -> Optional[int]:
        """
        Возвращает идентификатор пользователя из таблице "users"
        если такой пользователь существует.
        Args:
            user_id (int): Идентификатор записи в таблице "users".
            user_uuid (str): UUID пользователя в таблицу "users".

        Returns:
            Optional[int]: Идентификатор пользователя в таблице "users" базы данных.
        """
        query = select(UserModel.id).where(UserModel.id == user_id, UserModel.uuid == user_uuid)
        async with database.session() as session:
            result = await session.execute(query)
            await session.commit()
            row = result.first()
            if row:
                named_tuple = row.tuple()
                return named_tuple.id
