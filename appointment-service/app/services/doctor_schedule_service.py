from app.models import DoctorSchedule
from app.extensions import db

class DoctorScheduleService:
    @staticmethod
    def add_schedule(doctor_id, data):
        schedule = DoctorSchedule(
            doctor_id=doctor_id,
            weekday=data['weekday'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule

    @staticmethod
    def get_schedule(doctor_id):
        return DoctorSchedule.query.filter_by(doctor_id=doctor_id).all()
