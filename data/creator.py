from dataclasses import dataclass
from data.user import User
from datetime import datetime

@dataclass
class Creator(User):
    type: str= ""
    link: str= ""
    business_email: str= ""
    description: str= ""


    # def __post_init__(self):
    #     if not self.member_since:
    #         self.member_since = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        developer_dict = super().to_dict()
        developer_dict.update({
            'type': self.type,
            'link': self.link,
            'business_email': self.business_email,
            'description': self.description
        })
        return developer_dict
