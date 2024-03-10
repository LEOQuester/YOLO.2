from dataclasses import dataclass
@dataclass
class Admin:
    email: str = None
    password: bytes = None
    name: str = None

    def to_dict(self):
        Admin_dict = {
            'email': self.email,
            'password': self.password,
            'name': self.name,
        }
        # Set None values to empty string
        for key, value in Admin_dict.items():
            if value is None:
                Admin_dict[key] = ''
        return Admin_dict
