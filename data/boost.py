from dataclasses import dataclass

@dataclass
class Boost:
    title: str = None
    content_url: dict = None
    email: str = None
    keywords: list = None
    status: str = None  # approved / rejected / pending / paid
    timestamp: str = None


    def to_dict(self):
        return {
            'title': self.title,
            'content_url': self.content_url,
            'email': self.email,
            'keywords': self.keywords,
            'status': self.status,
            'timestamp': self.timestamp
        }
