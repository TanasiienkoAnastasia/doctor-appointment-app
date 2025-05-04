from collections import Counter
from datetime import datetime, timedelta

from app.models import User, Appointment
from app.services import AppointmentService


class DoctorService:
    @staticmethod
    def get_appointments_for_doctor(email):
        doctor = User.query.filter_by(email=email).first()
        if not doctor:
            return []
        return Appointment.query.filter_by(doctor_id=doctor.id).all()

    @staticmethod
    def get_all_doctors():
        return User.query.filter_by(user_type='doctor').all()

    @staticmethod
    def get_popular_slots_and_availability(doctor_id):
        start_date = datetime.today().date() - timedelta(days=30)
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.date >= start_date,
            Appointment.status != 'скасовано'
        ).all()

        slot_counter = Counter(str(a.time) for a in appointments)

        available = AppointmentService.get_available_slots_for_doctor(doctor_id)

        return {
            "top_slots": slot_counter.most_common(5),
            "free_today": len(available.get(str(datetime.today().date()), []))
        }
