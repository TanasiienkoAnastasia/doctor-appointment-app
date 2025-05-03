from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from app.guards.role_required import role_required
from app.utils import success, error
from app.schemas import CreateAppointmentSchema, AppointmentSchema
from app.services import AppointmentService
from flask import current_app

patient_appointments_routes = Blueprint('appointment_routes', __name__)

@role_required('patient')
@patient_appointments_routes.route('/patient/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    schema = CreateAppointmentSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return error("Помилка валідації", err.messages)

    user_payload = get_jwt()
    patient_id = user_payload.get('id')

    if not patient_id or patient_id != data['patient_id']:
        return error("Ви не можете створити прийом від імені іншого пацієнта", status=403)

    appointment = AppointmentService.create_appointment(data)
    return success("Прийом створено", AppointmentSchema().dump(appointment), status=201)

@patient_appointments_routes.route('/patient/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    user_payload = get_jwt()

    print(user_payload)
    patient_email = user_payload.get('email')
    appointments = AppointmentService.get_appointments_for_patient(patient_email)
    return success(data=AppointmentSchema(many=True).dump(appointments))

@jwt_required()
@patient_appointments_routes.route('/patient/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = AppointmentService.get_by_id(appointment_id)
    if not appointment:
        return error("Прийом не знайдено", status=404)

    if appointment.status == 'скасовано':
        return error("Неможливо редагувати скасований прийом", status=403)

    try:
        data = request.get_json()
        if not data:
            return error("Невірний формат даних", status=400)

        appointment = AppointmentService.update_appointment(appointment, data)
        return success("Прийом оновлено", AppointmentSchema().dump(appointment))

    except Exception as e:
        current_app.logger.error(f"Помилка оновлення прийому {appointment_id}: {str(e)}")
        return error("Сталася помилка під час оновлення", status=500)

@jwt_required()
@patient_appointments_routes.route('/patient/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = AppointmentService.get_by_id(appointment_id)
    if not appointment:
        return error("Прийом не знайдено", status=404)

    AppointmentService.delete_appointment(appointment)
    return success("Прийом видалено")
