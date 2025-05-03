from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from app.guards.role_required import role_required
from app.utils import success
from app.services import DoctorService
from app.schemas import AppointmentSchema, UserSchema

doctor_routes = Blueprint('doctor_routes', __name__)

@role_required('doctor')
@doctor_routes.route('/appointments', methods=['GET'])
@jwt_required()
def get_doctor_appointments():
    user_payload = get_jwt()

    print(user_payload)
    doctor_email = user_payload.get('email')
    appointments = DoctorService.get_appointments_for_doctor(doctor_email)

    return success(data=AppointmentSchema(many=True).dump(appointments))

@doctor_routes.route('/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    doctors = DoctorService.get_all_doctors()
    return success(data=UserSchema(many=True).dump(doctors))