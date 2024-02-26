from data.developer import Developer
from service.user_service import UserService
from repo.FirebaseDriver import FirebaseDriver
import uuid

class DeveloperService:
    def __init__(self):
        self.__driver = FirebaseDriver()
        self.__user_service = UserService()

    def createDeveloper(self, email, upasswordhash):
        #get developers from db
        developers = self.__driver.find_by_parameter("users", {"email": email})
        #validations
        if not developers:
            return {"success": False, "message": "User not found", "user": None}
        developer_data = developers[0]

        developer = Developer(
            email=developer_data['email'],
            agree=developer_data.get('agree'),
            country=developer_data.get('country'),
            password = developer_data.get('password'),
            name=developer_data.get('name'),
            premium=developer_data.get('premium'),
            region=developer_data.get('region'),
            role=developer_data.get('role'),
            contact_number=developer_data.get('contact_number')
        )

        if not self.__user_service.verify_password(upasswordhash.encode('utf-8'), developer_data.get('password')):
            return {"success": False, "message": "Invalid email or password", "user": None}
        
        #proceed with other steps
        developer.role = "developer"
        new_uuid = uuid.uuid4()
        uuid_str = str(new_uuid)
        developer.api_key = uuid_str 
        self.__driver.update_document('users', developer_data.get("doc_id"), developer.to_dict())
        return {"success": True, "message": "user found and developer unlocked", "api_key": developer.api_key}
    
    def save_request(self, api_key):
        return True