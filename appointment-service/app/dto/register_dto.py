from app.models import User
from werkzeug.security import generate_password_hash

class RegisterRequestDTO:
    def __init__(self, name, email, password, userType, phone=None, specialty=None, age=None):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = userType
        self.phone = phone
        self.specialty = specialty
        self.age = age

    def to_model(self):
        return User(
            username=self.name,
            email=self.email,
            password=generate_password_hash(self.password),
            user_type=self.user_type,
            phone=self.phone,
            specialty=self.specialty,
            age=self.age
        )
