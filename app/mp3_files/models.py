from uuid import uuid4
from datetime import datetime


from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Uuid,
    DateTime
)

from app.store.database.sqlalchemy_base import db
from sqlalchemy.orm import relationship


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
