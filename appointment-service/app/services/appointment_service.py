from app.extensions import db
from app.models import Appointment

class AppointmentService:
    @staticmethod
    def create_appointment(data):
        appointment = Appointment(**data)
        db.session.add(appointment)
        db.session.commit()
        return appointment

    @staticmethod
    def get_all():
        return Appointment.query.all()

    @staticmethod
    def get_by_id(appointment_id):
        return Appointment.query.get(appointment_id)

    @staticmethod
    def update_appointment(appointment, data):
        appointment.status = data.get('status', appointment.status)
        db.session.commit()
        return appointment

    @staticmethod
    def delete_appointment(appointment):
        db.session.delete(appointment)
        db.session.commit()
