from app.extensions import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False)
