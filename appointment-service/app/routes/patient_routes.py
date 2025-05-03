from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models import User

patient_blueprint = Blueprint('patient', __name__)

@patient_blueprint.route('/patient/profile', methods=['GET'])
@jwt_required()
def get_patient_profile():
    user_payload = get_jwt()

    print(user_payload)
    email = user_payload.get('email')
    user = User.query.filter_by(email=email).first()

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
