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
    complaint = request.args.get('complaint')

    if not complaint:
        return error("Параметр 'complaint' обов'язковий", status=400)

    # specialties = INJURY_SPECIALTIES.get(complaint.lower(), [])
    # if not specialties:
    #    return success("Рекомендацій не знайдено", data=[])

    doctors = User.query.filter(
        User.user_type == 'doctor',
        #User.specialty.in_(specialties) temporarily pass all doctors to frontend
    ).all()

    doctor_data = [
        {
            'id': d.id,
            'name': d.name,
            'surname': d.surname,
            'middle_name': d.middle_name,
            'email': d.email,
            'specialty': d.specialty
        }
        for d in doctors
    ]

    return success(data=doctor_data)
