from marshmallow import Schema, fields, validate

class CreateScheduleSchema(Schema):
    weekday = fields.String(required=True, validate=validate.OneOf(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)

    class Meta:
        ordered = True