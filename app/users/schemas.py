from marshmallow import Schema, fields, validate


from app.web.schemes import OkResponseSchema


class UserSchema(Schema):
    """
    Кдасс Schema для пользователя.
    """
    id = fields.Int()
    uuid = fields.UUID()
    username = fields.Str()


class UserRequestSchema(Schema):
    """
    Класс Schema представляет тело POST-запроса для конечной точки /users.create.
    """
    username = fields.Str(required=True, allow_none=False,
                          validate=[validate.Length(min=1, error="Field cannot be blank")])


class UserResponseSchema(OkResponseSchema):
    """
    Класс Schema представляет ответ на POST-запроса для конечной точки /users.create.
    """
    data = fields.Nested(UserSchema)
