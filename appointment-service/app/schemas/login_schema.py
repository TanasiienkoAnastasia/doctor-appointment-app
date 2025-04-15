from marshmallow import Schema, fields, validate, post_load
from app.dto.login_dto import LoginRequestDTO

class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

    @post_load
    def make_dto(self, data, **kwargs):
        return LoginRequestDTO(**data)
