from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from datetime import datetime


from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Uuid,
    DateTime,
    insert,
    select
)

from app.store.database.sqlalchemy_base import db
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.store.database.database import Database


class Mp3FileModel(db):
    """
    Класс, отображающий mp3 файлы в таблице "mp3_files" базы данных.
    Таблица "mp3_files" имеет отношение many-to-one с таблицей "users".
    Args:
        id: идентификатор записи.
        uuid: UUID.
        created_at: время создания записи.
        file_path: путь к файлу в файловом хранилище.
        filename: имя файла.
        user_id: идентификатор записи в таблице "users".
        user: экземпляр класс UserModel.
    """
    __tablename__ = "mp3_files"
    id = Column(Integer(), primary_key=True)
    uuid = Column(Uuid(as_uuid=True), default=uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    file_path = Column(String(), nullable=False)
    filename = Column(String(), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("UserModel", back_populates="mp3_files")

    @staticmethod
    async def inser_file(database: "Database", user_id: int, file_path: str, filename: str) -> "Mp3FileModel":
        """
        Добавляет новй файл в таблицу "mp3_files" базы данных.
        Returns:
            Возвращает идентификатор записи id в базе данных.
        """

        query = (insert(Mp3FileModel)
                 .returning(Mp3FileModel)
                 .values(file_path=file_path, user_id=user_id, filename=filename))
        async with database.session() as session:
            result = await session.execute(query)
            await session.commit()
            mp3_file_model = result.scalar_one()
            return mp3_file_model

    @staticmethod
    async def get_mp3_by_user(database: "Database", user_id: int, record_id: int) -> Optional["Mp3FileModel"]:
        """
        Делает запрос к базе данных и возвращает запись из таблице "mp3_files" базы данных.
        Если запись не существует, возвращает None.
        Args:
            record_id - идентификатор mp3 файла в базе данных.
            user_id - идентификатор пользователя в базе данных.
        """

        query = select(Mp3FileModel).where(Mp3FileModel.id == record_id,
                                           Mp3FileModel.user_id == user_id)
        async with database.session() as session:
            result = await session.execute(query)
            await session.commit()
            mp3_model = result.scalar_one_or_none()
            return mp3_model
