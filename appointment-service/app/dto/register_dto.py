from werkzeug.security import generate_password_hash
from app.models import User

class RegisterRequestDTO:
    def __init__(self, name, surname, middle_name, email, password, userType, phone=None, specialty=None, age=None, photo_url=None):
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.email = email
        self.password = password
        self.user_type = userType
        self.phone = phone
        self.specialty = specialty
        self.age = age
        self.photo_url = photo_url

    def to_model(self):
        return User(
            name=self.name,
            surname=self.surname,
            middle_name=self.middle_name,
            email=self.email,
            password=generate_password_hash(self.password),
            user_type=self.user_type,
            phone=self.phone,
            specialty=self.specialty,
            age=self.age,
            photo_url=self.photo_url  # ✅ нове поле
        )

