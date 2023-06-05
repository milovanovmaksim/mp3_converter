from aiohttp_apispec import docs, request_schema, response_schema
from app.store.users.accessor import UserAccessor

from app.users.schemas import UserRequestSchema, UserResponseSchema
from app.web.bases import View
from app.web.utils import json_response


class UserCreteView(View):
    """
    Класс представление для конечной точки "/user.create.

    Args:
        View (_type_): Базовый класс представление.
    """

    @docs(tags=["users"], summary="Create new user.")
    @request_schema(UserRequestSchema)
    @response_schema(UserResponseSchema, 200)
    async def post(self):
        """
        Вью-метод для POST-запроса.
        Метод декорируется "@response_schema", "@docs", "@request_schema" с целью добавления информации о запросе
        в спецификацию Swagger и промежуточное программное обеспечение validation_middleware для валидации данных.

        Returns:
            _type_: Возвращает экземпляр класса aiohttp.web_response.Response.
        """
        data = self.data
        username = data["username"]
        user_accessor = UserAccessor(self.request.app)
        user = await user_accessor.add_user(data={"username": username})
        return json_response(UserResponseSchema(), data={"data": user})
