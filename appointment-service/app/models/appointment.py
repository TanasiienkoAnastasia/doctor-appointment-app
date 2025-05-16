from app.extensions import db
from sqlalchemy import CheckConstraint

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    complaint = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    medical_data = db.Column(db.Text, nullable=True)  # ✅ нове поле

    __table_args__ = (
        CheckConstraint(
            status.in_(['scheduled', 'пішно', 'запізнення']),
            name='check_valid_status'
        ),
    )
