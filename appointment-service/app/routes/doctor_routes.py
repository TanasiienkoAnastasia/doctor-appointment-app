from datetime import time, timedelta, datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from app.guards.role_required import role_required
from app.models import Appointment
from app.utils import success, error
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

@doctor_routes.route('/<int:doctor_id>/available-slots', methods=['GET'])
@jwt_required()
def get_available_slots(doctor_id):
    date_str = request.args.get('date')
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return error("Невірний формат дати", status=400)

    appointments = Appointment.query.filter_by(doctor_id=doctor_id, date=date_obj).all()
    busy_times = {a.time for a in appointments}

    start = time(9, 0)
    end = time(17, 30)
    step = timedelta(minutes=30)

    slots = []
    current = datetime.combine(date_obj, start)
    end_dt = datetime.combine(date_obj, end)

    while current <= end_dt:
        if current.time() not in busy_times:
            slots.append(current.strftime("%H:%M"))
        current += step

    return success(data=slots)