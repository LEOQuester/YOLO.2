from data.collection import Collection
from repo.FirebaseDriver import FirebaseDriver


class CollectionService:
    def __init__(self):
        self.__driver = FirebaseDriver()

    def create_collection(self, collection : Collection):
        if self.__driver.create_document("collections", collection.to_dict()):
            return {"success": True, "message": "Collection Saved!"}
        return {"success": False, "message": "Error Occured!"}
    
    def get_all_collections(self):
        return self.__driver.get_all_documents("collections")
            
