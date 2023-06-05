import json
from typing import List

from aiohttp_apispec import docs, response_schema, querystring_schema
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web import Response
from marshmallow.exceptions import ValidationError

from app.store.users.accessor import UserAccessor
from app.web.bases import View
from app.mp3_files.schemas import Mp3FileShcemaResponse, Mp3FileShcemaRequest, RequestMp3DownloadFileSchema
from app.web.utils import error_json_response, json_response
from app.store.mp3_files.accessor import Mp3ConverterAccessor, Mp3FileDbAccessor
from app.web.utils import file_sender


class ConvertFileView(View):
    """
    Класс представление для конечной точки "/files.convert".

    Args:
        View (_type_): Базовый класс представление.
    """

    @docs(tags=["files"], summary="Convert a WAV format file to a mp3 format file.")
    @response_schema(Mp3FileShcemaResponse, 200)
    async def post(self):
        """
        Вью-метод для POST-запроса.
        Метод декорируется "@response_schema", "@docs" с целью добавления информации о запросе
        в спецификацию Swagger и промежуточное программное обеспечение validation_middleware для валидации данных.

        Raises:
            HTTPBadRequest: Возбуждает исключение в случае невалидных данных в POST-запросе от клиента.
            Исключение отлавливается в app.web.middlewares.error_handling_middleware и отправляется клиенту
            соответствующий ответ.
        Returns:
            _type_: Возвращает экземпляр класса aiohttp.web_response.Response.
        """
        user_id = self.request.headers.get("user_id")
        user_uuid = self.request.headers.get("user_uuid")
        data = {"user_id": user_id, "user_uuid": user_uuid}
        try:
            Mp3FileShcemaRequest().loads(json.dumps(data))
        except ValidationError as e:
            return error_json_response(http_status=400,
                                       status="bad request",
                                       data=e.messages_dict,
                                       message="Unprocessable Entity")

        user_accessor = UserAccessor(self.request.app)
        user_id = await user_accessor.get_user_id(int(user_id), user_uuid)  # type: ignore
        if not user_id:
            return error_json_response(http_status=404,
                                       status="not found",
                                       message="User not found")
        multipart_reader = await self.request.multipart()
        body_part_reader = await multipart_reader.next()
        if body_part_reader:
            filename = body_part_reader.filename  # type: ignore
            if filename:
                res: List[str] = filename.rsplit(".", maxsplit=1)
                filename: str = res[0]
                mp3_accessor = Mp3ConverterAccessor(filename, self.request.app, user_id)
                url = await mp3_accessor.run(body_part_reader)
                return json_response(Mp3FileShcemaResponse(), data={"url": url})
        raise HTTPBadRequest(reason="File is required.")


class DownloadMp3FileView(View):
    """
    Класс представление для конечной точки
    /files.record?record_id=id_записи&user_id=id_пользователя

    Args:
        View (_type_): Базовый класс представление.
    """
    @docs(tags=["files"], summary="Download mp3 file.")
    @querystring_schema(RequestMp3DownloadFileSchema)
    async def get(self):
        """
        Вью-метод для GET-запроса.
        Метод декорируется "@querystring_schema", "@docs" с целью добавления информации о запросе
        в спецификацию Swagger и промежуточное программное обеспечение validation_middleware для валидации данных.

        Returns:
            _type_: Возвращает экземпляр класса aiohttp.web_response.Response.
        """
        data = self.query
        mp3_file_accessor = Mp3FileDbAccessor(self.request.app)
        mp3_model = await mp3_file_accessor.get_mp3_by_user(**data)
        if not mp3_model:
            return error_json_response(http_status=404,
                                       status="not found",
                                       message="User or required mp3 file not found")
        headers = {
            "Content-disposition": f"attachment; filename={mp3_model.filename}"
        }
        body = file_sender(file_name=mp3_model.file_path)
        return Response(
            body=body,
            headers=headers
        )
