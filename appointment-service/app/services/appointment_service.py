from datetime import timedelta, datetime, time

from app.extensions import db
from app.models import Appointment, User


class AppointmentService:
    @staticmethod
    def create_appointment(data):
        doctor_id = data["doctor_id"]
        desired_date = data["date"]
        desired_time = data["time"]

        next_date, next_time = AppointmentService.find_next_available_slot(doctor_id, desired_date, desired_time)

        data["date"] = next_date
        data["time"] = next_time

        appointment = Appointment(**data)
        db.session.add(appointment)
        db.session.commit()
        return appointment

    @staticmethod
    def find_next_available_slot(doctor_id, start_date, start_time):
        max_days_ahead = 30
        duration = timedelta(minutes=30)
        slots = AppointmentService.generate_time_slots(start=time(9, 0), end=time(17, 30), step_minutes=30)

        for offset in range(max_days_ahead):
            current_date = start_date + timedelta(days=offset)

            appointments = Appointment.query.filter_by(
                doctor_id=doctor_id,
                date=current_date
            ).order_by(Appointment.time).all()

            busy_slots = set(a.time for a in appointments if a.status != 'скасовано')

            for slot in slots:
                if offset == 0 and slot < start_time:
                    continue

                if slot not in busy_slots:
                    return current_date, slot

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
        new_date = data.get('date', appointment.date)
        new_time = data.get('time', appointment.time)
        new_doctor_id = data.get('doctor_id', appointment.doctor_id)

        conflict = Appointment.query.filter_by(
            doctor_id=new_doctor_id,
            date=new_date,
            time=new_time
        ).filter(
            Appointment.id != appointment.id,
            Appointment.status != 'скасовано'
        ).first()

        if conflict:
            raise ValueError("Цей слот уже зайнятий у розкладі лікаря")

        appointment.status = data.get('status', appointment.status)
        appointment.date = new_date
        appointment.time = new_time
        appointment.complaint = data.get('complaint', appointment.complaint)
        appointment.comment = data.get('comment', appointment.comment)
        appointment.doctor_id = new_doctor_id

        db.session.commit()
        return appointment

    @staticmethod
    def delete_appointment(appointment):
        db.session.delete(appointment)
        db.session.commit()
