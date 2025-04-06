from flask import Blueprint, request, jsonify
from app.models import MedicalRecord
from app import db
from flask import Blueprint, jsonify

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "service": "medical-records-service"}), 200

medical_routes = Blueprint('medical_routes', __name__)

@medical_routes.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Medical Records Service is running'}), 200

@medical_routes.route('/records', methods=['POST'])
def create_record():
    data = request.get_json()
    record = MedicalRecord(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        diagnosis=data['diagnosis'],
        treatment=data.get('treatment')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Record created'}), 201

@medical_routes.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = MedicalRecord.query.get(record_id)
    if not record:
        return jsonify({'message': 'Not found'}), 404

    return jsonify({
        'id': record.id,
        'patient_id': record.patient_id,
        'doctor_id': record.doctor_id,
        'diagnosis': record.diagnosis,
        'treatment': record.treatment,
        'created_at': record.created_at
    })

@medical_routes.route('/records', methods=['GET'])
def get_all_records():
    records = MedicalRecord.query.all()
    return jsonify([{
        'id': r.id,
        'patient_id': r.patient_id,
        'doctor_id': r.doctor_id,
        'diagnosis': r.diagnosis,
        'treatment': r.treatment,
        'created_at': r.created_at
    } for r in records])
