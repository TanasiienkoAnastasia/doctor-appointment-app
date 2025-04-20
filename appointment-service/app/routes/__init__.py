from .auth_routes import auth_routes
from .user_routes import user_routes
from .patient_appointments_routes import patient_appointments_routes
from .recommendation_routes import recommendation_routes
from .doctor_routes import doctor_routes

__all__ = [
    'auth_routes',
    'user_routes',
    'patient_appointments_routes',
    'recommendation_routes',
    'doctor_routes',
]