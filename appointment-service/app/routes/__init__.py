from .auth_routes import auth_routes
from .user_routes import user_routes
from .patient_appointments_routes import patient_appointments_routes

__all__ = [
    'auth_routes',
    'user_routes',
    'patient_appointments_routes',
    'recommendation_routes',
    'doctor_routes',
]