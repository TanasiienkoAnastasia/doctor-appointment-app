from marshmallow import Schema, fields
from app.schemas.user_schema import UserSchema

class CreateAppointmentSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    complaint = fields.Str(required=True)
    status = fields.Str(missing='scheduled')

    class Meta:
        ordered = True


class AppointmentSchema(Schema):
    id = fields.Int()
    doctor_id = fields.Int()
    patient_id = fields.Int()
    date = fields.Date()
    time = fields.Time()
    complaint = fields.Str()
    status = fields.Str()

    doctor = fields.Nested(UserSchema, only=("id", "username", "specialty"))
    patient = fields.Nested(UserSchema, only=("id", "username", "age"))

    class Meta:
        ordered = True
