from dataclasses import dataclass
from data.user import User
from datetime import datetime

@dataclass
class Creator(User):
    member_since: str = None
    creator: bool = True
    sm_links: dict = None

    def __post_init__(self):
        if not self.member_since:
            self.member_since = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        developer_dict = super().to_dict()
        developer_dict.update({
            'api_key': self.api_key,
            'quota': self.quota,
            'member_since': self.member_since,
            'creator': self.creator,
            'sm_links': self.sm_links
        })
        return developer_dict
