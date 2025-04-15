from flask import Blueprint, request
from marshmallow import ValidationError
from app.utils import success, error
from app.schemas import CreateAppointmentSchema, AppointmentSchema
from app.services import AppointmentService
from app.guards.jwt_required import jwt_required

appointment_routes = Blueprint('appointment_routes', __name__)

@jwt_required
@appointment_routes.route('/appointments', methods=['POST'])
def create_appointment():
    schema = CreateAppointmentSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return error("Помилка валідації", err.messages)

    appointment = AppointmentService.create_appointment(data)
    return success("Прийом створено", AppointmentSchema().dump(appointment), status=201)

@jwt_required
@appointment_routes.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = AppointmentService.get_all()
    return success(data=AppointmentSchema(many=True).dump(appointments))

@jwt_required
@appointment_routes.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = AppointmentService.get_by_id(appointment_id)
    if not appointment:
        return error("Прийом не знайдено", status=404)

    data = request.get_json()
    appointment = AppointmentService.update_appointment(appointment, data)
    return success("Прийом оновлено", AppointmentSchema().dump(appointment))

@jwt_required
@appointment_routes.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = AppointmentService.get_by_id(appointment_id)
    if not appointment:
        return error("Прийом не знайдено", status=404)

    AppointmentService.delete_appointment(appointment)
    return success("Прийом видалено")
