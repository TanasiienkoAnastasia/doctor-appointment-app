from .auth_routes import auth_routes
from .user_routes import user_routes
from .appointment_routes import appointment_routes
from .schedule_routes import schedule_routes
from .medical_records_routes import medical_records_routes

__all__ = [
    'auth_routes',
    'user_routes',
    'appointment_routes',
    'schedule_routes',
    'medical_records_routes',
]