from marshmallow import Schema, fields, validate, post_load
from app.dto.register_dto import RegisterRequestDTO

class RegisterRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    userType = fields.String(required=True, validate=validate.OneOf(["patient", "doctor"]))
    phone = fields.String(required=False, allow_none=True, validate=validate.Length(min=7, max=20))
    specialty = fields.String(required=False, allow_none=True, validate=validate.Length(min=2, max=100))
    age = fields.Int(validate=validate.Range(min=0, max=120), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_dto(self, data, **kwargs):
        return RegisterRequestDTO(**data)
