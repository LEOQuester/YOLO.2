from dataclasses import dataclass
@dataclass
class User:
    email: str = None
    agree: bool = None
    password: bytes = None
    country: str = None
    name: str = None
    premium: bool = None
    region: str = None
    role: str = None
    contact_number: str = None

    def to_dict(self):
        user_dict = {
            'email': self.email,
            'agree': self.agree,
            'password': self.password,
            'country': self.country,
            'name': self.name,
            'premium': self.premium,
            'region': self.region,
            'role': self.role,
            'contact_number': self.contact_number
        }
        # Set None values to empty string
        for key, value in user_dict.items():
            if value is None:
                user_dict[key] = ''
        return user_dict
