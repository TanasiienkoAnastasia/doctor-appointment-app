from marshmallow import Schema, fields

class CreateAppointmentSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    appointment_time = fields.DateTime(required=True)
    status = fields.Str(missing='scheduled')

    class Meta:
        ordered = True