from dataclasses import dataclass

@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    user_type: str

    @staticmethod
    def from_model(user):
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            user_type=user.user_type
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "userType": self.user_type
        }
