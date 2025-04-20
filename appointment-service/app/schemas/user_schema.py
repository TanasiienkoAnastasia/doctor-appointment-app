from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    user_type = fields.Str(data_key="userType", required=True)
    phone = fields.Str(allow_none=True)
    specialty = fields.Str(allow_none=True)
    age = fields.Int(allow_none=True)  # якщо плануєш додавати в модель

    class Meta:
        ordered = True
