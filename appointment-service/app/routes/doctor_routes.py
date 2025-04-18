from flask import Blueprint, request
from app.guards.jwt_required import jwt_required
from app.guards.role_required import role_required
from app.utils.response_utils import success
from app.services.doctor_service import DoctorService
from app.schemas import AppointmentSchema

doctor_routes = Blueprint('doctor_routes', __name__)

@jwt_required
@role_required('doctor')
@doctor_routes.route('/appointments', methods=['GET'])
def get_doctor_appointments():
    user_payload = request.user

    doctor_email = user_payload.get('email')
    appointments = DoctorService.get_appointments_for_doctor(doctor_email)

    return success(data=AppointmentSchema(many=True).dump(appointments))