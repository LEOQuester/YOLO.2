from dataclasses import dataclass
from data.user import User

@dataclass
class Developer(User):
    api_key: str = None
    quota: int = 1000

    def to_dict(self):
        developer_dict = super().to_dict()
        developer_dict.update({
            'api_key': self.api_key,
            'quota': self.quota
        })
        return developer_dict