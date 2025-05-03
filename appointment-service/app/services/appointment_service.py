from app.extensions import db
from app.models import Appointment, User


class AppointmentService:
    @staticmethod
    def create_appointment(data):
        appointment = Appointment(**data)
        db.session.add(appointment)
        db.session.commit()
        return appointment

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
