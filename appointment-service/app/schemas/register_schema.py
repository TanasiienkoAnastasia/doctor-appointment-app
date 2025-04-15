from marshmallow import Schema, fields, validate

class RegisterRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2),
                         error_messages={"required": "Ім'я є обов'язковим"})
    email = fields.Email(required=True, error_messages={"required": "Email обов'язковий"})
    password = fields.String(required=True, validate=validate.Length(min=6),
                             error_messages={"required": "Пароль обов'язковий"})
    userType = fields.String(required=True, validate=validate.OneOf(["patient", "doctor"]),
                             error_messages={"required": "Тип користувача обов'язковий"})
