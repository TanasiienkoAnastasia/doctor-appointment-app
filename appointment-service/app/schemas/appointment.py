from marshmallow import Schema, fields, validate
from app.schemas.user_schema import UserSchema

class CreateAppointmentSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    complaint = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(["scheduled", "пішно", "запізнення"]))
    comment = fields.Str(required=False)
    medical_data = fields.Str(required=False)  # 🔹 нове поле

    class Meta:
        ordered = True


class AppointmentSchema(Schema):
    id = fields.Int()
    doctor_id = fields.Int()
    patient_id = fields.Int()
    date = fields.Date()
    time = fields.Time()
    complaint = fields.Str()
    status = fields.Str(validate=validate.OneOf(["scheduled", "пішно", "запізнення"]))
    comment = fields.Str(required=False)
    medical_data = fields.Str(required=False)  # 🔹 нове поле

    doctor = fields.Nested(UserSchema, only=("id", "name", "surname", "middle_name", "specialty", "phone"))
    patient = fields.Nested(UserSchema, only=("id", "name", "surname", "middle_name", "age", "phone"))

    class Meta:
        ordered = True
