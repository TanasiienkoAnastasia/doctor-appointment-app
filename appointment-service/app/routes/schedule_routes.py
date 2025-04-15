from flask import Blueprint, request
from marshmallow import ValidationError
from app.models import User
from app.services import DoctorScheduleService
from app.schemas import CreateScheduleSchema, DoctorScheduleSchema
from app.utils import success, error
from app.guards.jwt_required import jwt_required

schedule_routes = Blueprint('schedule_routes', __name__)

@jwt_required
@schedule_routes.route('/schedule', methods=['POST'])
def add_schedule():
    schema = CreateScheduleSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return error("Помилка валідації", err.messages)

    doctor_email = request.user.get("email")
    doctor_id = User.query.filter_by(email=doctor_email).first().id

    schedule = DoctorScheduleService.add_schedule(doctor_id, data)
    schedule_data = DoctorScheduleSchema().dump(schedule)

    return success("Розклад додано", schedule_data, status=201)

@jwt_required
@schedule_routes.route('/schedule/<int:doctor_id>', methods=['GET'])
def get_schedule(doctor_id):
    schedules = DoctorScheduleService.get_schedule(doctor_id)
    schedule_data = DoctorScheduleSchema(many=True).dump(schedules)
    return success(data=schedule_data)
