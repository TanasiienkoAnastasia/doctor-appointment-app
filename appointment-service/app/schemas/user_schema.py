from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    middle_name = fields.Str(required=True, data_key="middleName")
    email = fields.Email(required=True)
    user_type = fields.Str(data_key="userType", required=True)
    phone = fields.Str(allow_none=True)
    specialty = fields.Str(allow_none=True)
    age = fields.Int(allow_none=True)

    class Meta:
        ordered = True
