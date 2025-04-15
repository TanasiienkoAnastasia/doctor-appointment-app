class LoginRequestDTO:
    def __init__(self, data):
        self.errors = []

        self.email = data.get('email')
        self.password = data.get('password')

        self.validate()

    def validate(self):
        if not self.email or '@' not in self.email:
            self.errors.append("Невалідна електронна адреса.")
        if not self.password:
            self.errors.append("Пароль є обов'язковим.")

    def is_valid(self):
        return not self.errors
