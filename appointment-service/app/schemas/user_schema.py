from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    user_type = fields.Str(data_key="userType")
    phone = fields.Str(allow_none=True)
    specialty = fields.Str(allow_none=True)
