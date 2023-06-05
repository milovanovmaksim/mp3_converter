from marshmallow import Schema, fields, validate

from app.web.schemes import OkResponseSchema


class Mp3FileShcemaRequest(Schema):
    """
    Класс представляет заголовки POST-запроса для конечной точки /files.convert.
    """
    user_id = fields.Int(required=True, allow_none=False)
    user_uuid = fields.Str(required=True, allow_none=False,
                           validate=[validate.Length(min=1, error="Field cannot be blank")])


class Mp3FileShcemaResponse(OkResponseSchema):
    """
    Класс представляет ответ на POST-запроса для конечной точки /files.convert.
    """
    url = fields.Str()


class RequestMp3DownloadFileSchema(Schema):
    """
    Класс представляет параметры url адреса
    /files.record?record_id=id_записи&user_id=id_пользователя GET-запроса.

    """
    user_id = fields.Int(required=True, allow_none=False)
    record_id = fields.Int(required=True, allow_none=False)
