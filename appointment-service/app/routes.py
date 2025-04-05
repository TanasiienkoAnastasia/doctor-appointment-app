# appointment-service/app/routes.py
from flask import Blueprint, request, jsonify
from app.models import Appointment
from app import db
from datetime import datetime

appointment_routes = Blueprint('appointment_routes', __name__)

@appointment_routes.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Appointment Service is running'}), 200

@appointment_routes.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_time=datetime.fromisoformat(data['appointment_time']),
        status=data.get('status', 'scheduled')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify(appointment.to_dict()), 201

@appointment_routes.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])

@appointment_routes.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()
    appointment.status = data.get('status', appointment.status)
    db.session.commit()
    return jsonify(appointment.to_dict())

@appointment_routes.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted'})