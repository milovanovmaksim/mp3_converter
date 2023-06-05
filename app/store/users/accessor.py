from typing import Any, Optional
from sqlalchemy import insert, select

from app.base.base_accessor import BaseAccessor
from app.users.models import UserModel


class UserAccessor(BaseAccessor):
    """
    Класс, предоставляющий доступ к данным таблице "users" в базе данных.
    """

    async def add_user(self, data: dict[Any, Any]) -> UserModel:
        """
        Добавляет нового пользователя в таблицу "users" базы данных.
        Returns:
            Возвращает экземпляр класса UserModel.
        """

        query = insert(UserModel).values(**data).returning(UserModel)
        async with self.database.session() as session:
            result = await session.execute(query)
            await session.commit()
            user_model = result.scalar()
            return user_model

    async def get_user_id(self, user_id: int, user_uuid: str) -> Optional[int]:
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
        async with self.database.session() as session:
            result = await session.execute(query)
            await session.commit()
            row = result.first()
            if row:
                named_tuple = row.tuple()
                return named_tuple.id
