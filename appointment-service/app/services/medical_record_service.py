from app.models import MedicalRecord
from app.extensions import db

class MedicalRecordService:
    @staticmethod
    def create_record(data):
        record = MedicalRecord(**data)
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def get_by_id(record_id):
        return MedicalRecord.query.get(record_id)

    @staticmethod
    def get_all():
        return MedicalRecord.query.all()
