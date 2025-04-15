from flask import Blueprint, request
from marshmallow import ValidationError
from app.models import User
from app.services.doctor_schedule_service import DoctorScheduleService
from app.schemas import CreateScheduleSchema, DoctorScheduleSchema
from app.utils.response_utils import success, error
from app.guards.jwt_required import jwt_required
from app.guards.role_required import role_required

schedule_routes = Blueprint('schedule_routes', __name__)

@schedule_routes.route('/schedule', methods=['POST'])
@jwt_required
@role_required('doctor')
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

@schedule_routes.route('/schedule/<int:doctor_id>', methods=['GET'])
def get_schedule(doctor_id):
    schedules = DoctorScheduleService.get_schedule(doctor_id)
    schedule_data = DoctorScheduleSchema(many=True).dump(schedules)
    return success(data=schedule_data)
