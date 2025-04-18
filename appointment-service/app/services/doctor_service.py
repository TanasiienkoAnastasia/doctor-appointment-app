from app.models import User, Appointment

class DoctorService:
    @staticmethod
    def get_appointments_for_doctor(email):
        doctor = User.query.filter_by(email=email).first()
        if not doctor:
            return []
        return Appointment.query.filter_by(doctor_id=doctor.id).all()
