from datetime import timedelta, datetime, time

from app.extensions import db
from app.models import Appointment, User


class AppointmentService:
    @staticmethod
    def create_appointment(data):
        doctor_id = data["doctor_id"]
        desired_date = data["date"]
        desired_time = data["time"]

        slots = AppointmentService.generate_time_slots(start=time(9, 0), end=time(17, 30), step_minutes=30)

        for offset in range(0, 30):
            current_date = desired_date + timedelta(days=offset)
            existing_appointments = Appointment.query.filter_by(
                doctor_id=doctor_id,
                date=current_date
            ).order_by(Appointment.time).all()

            busy_slots = set(a.time for a in existing_appointments)

            for slot in slots:
                if offset == 0 and slot < desired_time:
                    continue

                if slot not in busy_slots:
                    data["date"] = current_date
                    data["time"] = slot
                    appointment = Appointment(**data)
                    db.session.add(appointment)
                    db.session.commit()
                    return appointment

        raise ValueError("Немає вільних слотів у лікаря протягом наступних 30 днів")

    @staticmethod
    def generate_time_slots(start: time, end: time, step_minutes: int):
        slots = []
        current = datetime.combine(datetime.today(), start)
        end_time = datetime.combine(datetime.today(), end)

        while current <= end_time:
            slots.append(current.time())
            current += timedelta(minutes=step_minutes)

        return slots

    @staticmethod
    def get_appointments_for_patient(email):
        patient = User.query.filter_by(email=email).first()
        if not patient:
            return []

        return Appointment.query.filter_by(patient_id=patient.id).all()

    @staticmethod
    def get_by_id(appointment_id):
        return Appointment.query.get(appointment_id)


    @staticmethod
    def update_appointment(appointment, data):
        appointment.status = data.get('status', appointment.status)
        appointment.date = data.get('date', appointment.date)
        appointment.time = data.get('time', appointment.time)
        appointment.complaint = data.get('complaint', appointment.complaint)
        appointment.comment = data.get('comment', appointment.comment)
        appointment.doctor_id = data.get('doctor_id', appointment.doctor_id)
        db.session.commit()
        return appointment

    @staticmethod
    def delete_appointment(appointment):
        db.session.delete(appointment)
        db.session.commit()
