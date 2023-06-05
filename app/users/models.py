from uuid import uuid4


from sqlalchemy import (
    Column,
    Integer,
    String,
    Uuid
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


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
