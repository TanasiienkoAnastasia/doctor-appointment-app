from marshmallow import Schema, fields, validate

class LoginRequestSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email обов'язковий"})
    password = fields.String(required=True, validate=validate.Length(min=6), error_messages={"required": "Пароль обов'язковий"})