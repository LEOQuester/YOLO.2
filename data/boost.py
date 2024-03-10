from dataclasses import dataclass

@dataclass
class Boost:
    content_type: str = None
    content_url: dict = None
    creator_doc_id: str = None
    keywords: list = None
    payment: bool = None
    status: str = None  # approved / rejected

    def to_dict(self):
        return {
            'content_type': self.content_type,
            'content_url': self.content_url,
            'creator_doc_id': self.creator_doc_id,
            'keywords': self.keywords,
            'payment': self.payment,
            'status': self.status,
        }
