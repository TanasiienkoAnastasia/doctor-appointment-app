from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=True)
    middle_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    specialty = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)



    appointments_as_doctor = db.relationship(
        'Appointment',
        foreign_keys='Appointment.doctor_id',
        backref='doctor',
        lazy=True
    )
    appointments_as_patient = db.relationship(
        'Appointment',
        foreign_keys='Appointment.patient_id',
        backref='patient',
        lazy=True
    )
