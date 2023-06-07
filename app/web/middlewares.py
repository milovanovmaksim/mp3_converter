import json
from typing import TYPE_CHECKING, Dict, Any, Optional

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware

from app.web.utils import error_json_response

if TYPE_CHECKING:
    from aiohttp.web import Request, Application

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    """
    Промежуточное ПО для обработки исключений в веб-приложении.
    """
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        data: Optional[Dict[Any, Any]] = None
        if e.text:
            data = json.loads(e.text)
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=data,
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=e.reason)
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message="internal server error")


def setup_middlewares(app: "Application"):
    """
    Устанавливает промежуточное программное обеспечение.

    Args:
        app (Application): Экземпляр класса Application.
    """
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
