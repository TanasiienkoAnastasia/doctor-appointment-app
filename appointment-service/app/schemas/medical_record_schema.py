from marshmallow import Schema, fields

class CreateMedicalRecordSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    diagnosis = fields.Str(required=True)
    treatment = fields.Str()

    class Meta:
        ordered = True

class MedicalRecordSchema(Schema):
    id = fields.Int()
    patient_id = fields.Int()
    doctor_id = fields.Int()
    diagnosis = fields.Str()
    treatment = fields.Str()
    created_at = fields.DateTime()

    class Meta:
        ordered = True
