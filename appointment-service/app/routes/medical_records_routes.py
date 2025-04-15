from flask import Blueprint, request
from marshmallow import ValidationError
from app.schemas import CreateMedicalRecordSchema, MedicalRecordSchema
from app.services import MedicalRecordService
from app.utils import success, error
from app.guards.jwt_required import jwt_required

medical_records_routes = Blueprint('medical_routes', __name__)

@jwt_required
@medical_records_routes.route('/records', methods=['POST'])
def create_record():
    schema = CreateMedicalRecordSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return error("Помилка валідації", err.messages)

    record = MedicalRecordService.create_record(data)
    return success("Запис створено", MedicalRecordSchema().dump(record), status=201)

@jwt_required
@medical_records_routes.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = MedicalRecordService.get_by_id(record_id)
    if not record:
        return error("Запис не знайдено", status=404)

    return success(data=MedicalRecordSchema().dump(record))

@jwt_required
@medical_records_routes.route('/records', methods=['GET'])
def get_all_records():
    records = MedicalRecordService.get_all()
    return success(data=MedicalRecordSchema(many=True).dump(records))
