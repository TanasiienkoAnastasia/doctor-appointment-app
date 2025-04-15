# app/dto/register_request_dto.py

class RegisterRequestDTO:
    def __init__(self, data):
        self.errors = []

        self.name = data.get('name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.user_type = data.get('userType')

        self.validate()

    def validate(self):
        if not self.name:
            self.errors.append("Ім'я є обов'язковим.")
        if not self.email or "@" not in self.email:
            self.errors.append("Невалідна електронна адреса.")
        if not self.password or len(self.password) < 6:
            self.errors.append("Пароль повинен містити щонайменше 6 символів.")
        if self.user_type not in ['patient', 'doctor']:
            self.errors.append("Неправильний тип користувача (допустимо: patient, doctor).")

    def is_valid(self):
        return not self.errors
