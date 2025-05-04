from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.schemas import UserSchema
from app.services import DoctorService
from app.services.doctor_recommendation_service import DoctorRecommendationService
from app.utils import success, error

recommendation_routes = Blueprint('recommendation_routes', __name__)

@jwt_required()
@recommendation_routes.route('/recommendations', methods=['GET'])
def get_recommendations():
    complaint = request.args.get('complaint')
    if not complaint:
        return error("Необхідно вказати скаргу", status=400)

    if len(complaint) < 10:
        return success(data=UserSchema(many=True).dump(DoctorService.get_all_doctors()))
    try:
        recommended_doctors = DoctorRecommendationService.recommend_doctors(complaint)
        if len(recommended_doctors) == 0:
            return success(data=UserSchema(many=True).dump(DoctorService.get_all_doctors()))

        return success(data=recommended_doctors)
    except Exception as e:
        return success(data=UserSchema(many=True).dump(DoctorService.get_all_doctors()))
