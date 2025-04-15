from marshmallow import Schema, fields, validate, post_load
from app.dto.register_dto import RegisterRequestDTO

class RegisterRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    userType = fields.String(required=True, validate=validate.OneOf(["patient", "doctor"]))

    @post_load
    def make_dto(self, data, **kwargs):
        return RegisterRequestDTO(**data)
