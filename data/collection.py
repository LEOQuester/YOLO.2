from dataclasses import dataclass
@dataclass
class Collections:
    contents: dict = None
    description: str = None
    duration: str = None
    Keywords: list = None
    title: str = None
    premium: bool = False

    def to_dict(self) -> dict:
        collection_dict = {
            'contents': self.contents,
            'Keywords': self.Keywords,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'premium': self.premium,
        }
        # Set None values to empty string or empty list
        for key, value in collection_dict.items():
            if value is None:
                if isinstance(value, list):
                    collection_dict[key] = []
                else:
                    collection_dict[key] = ''
        return collection_dict
