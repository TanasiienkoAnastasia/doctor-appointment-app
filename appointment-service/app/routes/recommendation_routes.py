from flask import Blueprint, request, jsonify
from app.models import User
from app.utils.response_utils import success, error
from app.guards.jwt_required import jwt_required

recommendation_routes = Blueprint('recommendation_routes', __name__)

INJURY_SPECIALTIES = {
    'перелом': ['травматолог', 'ортопед'],
    'вивих': ['травматолог', 'ортопед'],
    'розтягнення': ['травматолог'],
}

@recommendation_routes.route('/recommendations', methods=['GET'])
@jwt_required
def get_doctor_recommendations():
    injury = request.args.get('injury')

    if not injury:
        return error("Параметр 'injury' обов'язковий", status=400)

    specialties = INJURY_SPECIALTIES.get(injury.lower(), [])
    if not specialties:
        return success("Рекомендацій не знайдено", data=[])

    doctors = User.query.filter(
        User.user_type == 'doctor',
        User.specialty.in_(specialties)
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
