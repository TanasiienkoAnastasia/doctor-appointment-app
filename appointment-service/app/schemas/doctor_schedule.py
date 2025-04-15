from marshmallow import Schema, fields

class DoctorScheduleSchema(Schema):
    id = fields.Int()
    doctor_id = fields.Int()
    weekday = fields.Str()
    start_time = fields.Time()
    end_time = fields.Time()

    class Meta:
        ordered = True