from typing import Any, Optional, TYPE_CHECKING


from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response
import aiofiles


if TYPE_CHECKING:
    from marshmallow import Schema


def json_response(schema: "Schema", data: Optional[dict[Any, Any]] = None) -> Response:
    """
    Создает ответ в формате "application/json" для клиента на успешный get или post запросы.

    Args:
        schema (Schema): Класс schema, представляющий ответ на запрос от клиента.
        data (Optional[dict[Any, Any]], optional): Словарь, содержащий данные ответа на запрос клиента.

    Returns:
        Response: Возвращает экземпляр класса aiohttp.web_response.Response.
    """
    return Response(
        body=schema.dumps(data),
        headers={
            "Content-Type": "application/json",
        },
    )


def error_json_response(
    http_status: int,
    status: str,
    message: Optional[str] = None,
    data: Optional[dict] = None,
) -> Response:
    """
    Создает ответ в формате "application/json" для клиента на неуспешный get или post запросы.

    Args:
        http_status (int): Код ошибки.
        status (str): Строковое описание кода ошибки. (not found, bad request и.т.д)
        message (Optional[str], optional): Подробное описание ошибки. Почему она произошла.
        data (Optional[dict], optional): Словарь, содержащий в качестве ключа название переданного поля,
        а значением является описание ошибки для данного поля.

    Returns:
        _type_: Возвращает экземпляр класса aiohttp.web_response.Response.
    """
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={"code": http_status, "status": status, "message": message, "data": data},
    )


async def file_sender(file_name: str):
    """
    Асинхронный генератор для чтения данных из файлов частями.

    Args:
        file_name (str): Путь к файлу.

    Yields:
        _type_: Возвращает прочитанные байты.
    """
    async with aiofiles.open(file_name, mode='rb') as f:
        chunk = await f.read(5*1024*1024)
        while chunk:
            yield chunk
            chunk = await f.read(5*1024*1024)
