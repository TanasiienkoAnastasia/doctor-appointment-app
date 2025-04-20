from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models import User
from app.utils import success, error

recommendation_routes = Blueprint('recommendation_routes', __name__)

INJURY_SPECIALTIES = {
    'перелом': ['травматолог', 'ортопед'],
    'вивих': ['травматолог', 'ортопед'],
    'розтягнення': ['травматолог'],
}

@jwt_required()
@recommendation_routes.route('/recommendations', methods=['GET'])
def get_doctor_recommendations():
    injury = request.args.get('injury')

    if not injury:
        return error("Параметр 'injury' обов'язковий", status=400)

    specialties = INJURY_SPECIALTIES.get(injury.lower(), [])
    if not specialties:
        return success("Рекомендацій не знайдено", data=[])

    doctors = User.query.filter(
        User.user_type == 'doctor',
        #User.specialty.in_(specialties) temporarily pass all doctors to frontend
    ).all()

    doctor_data = [
        {
            'id': d.id,
            'name': d.username,
            'email': d.email,
            'specialty': d.specialty
        }
        for d in doctors
    ]

    return success(data=doctor_data)
