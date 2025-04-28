# app/routes/patient_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

patient_blueprint = Blueprint('patient', __name__)

@patient_blueprint.route('/patient/profile', methods=['GET'])
@jwt_required()
def get_patient_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "surname": user.surname,
        "middle_name": user.middle_name,
        "specialty": user.specialty,
        "age": user.age,
        "user_type": user.user_type
    }), 200
