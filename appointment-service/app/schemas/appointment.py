from marshmallow import Schema, fields

class AppointmentSchema(Schema):
    id = fields.Int()
    doctor_id = fields.Int()
    patient_id = fields.Int()
    appointment_time = fields.DateTime()
    status = fields.Str()

    class Meta:
        ordered = True