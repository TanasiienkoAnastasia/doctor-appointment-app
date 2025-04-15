from flask import Blueprint, request, jsonify
from app.models.doctor_schedule import DoctorSchedule
from app import db

schedule_routes = Blueprint('schedule_routes', __name__)

@schedule_routes.route('/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    schedule = DoctorSchedule(
        doctor_id=data['doctor_id'],
        weekday=data['weekday'],
        start_time=data['start_time'],
        end_time=data['end_time']
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify({"message": "Розклад додано"}), 201

@schedule_routes.route('/schedule/<int:doctor_id>', methods=['GET'])
def get_schedule(doctor_id):
    schedules = DoctorSchedule.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([{
        'weekday': s.weekday,
        'start_time': s.start_time.strftime('%H:%M'),
        'end_time': s.end_time.strftime('%H:%M')
    } for s in schedules])
