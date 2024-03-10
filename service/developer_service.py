from data.developer import Developer
from service.user_service import UserService
from repo.FirebaseDriver import FirebaseDriver
import uuid
import time

class DeveloperService:
    def __init__(self):
        self.__driver = FirebaseDriver()
        self.__user_service = UserService()
        self.__developer = Developer()

    def createDeveloper(self, email, upasswordhash):
        #get developers from db
        developers = self.__driver.find_by_parameter("users", {"email": email})
        #validations
        if not developers:
            return {"success": False, "message": "User not found", "user": None}
        developer_data = developers[0]

        self.__developer.email = developer_data.get('email')
        self.__developer.agree = developer_data.get('agree')
        self.__developer.country = developer_data.get('country')
        self.__developer.password = developer_data.get('password')
        self.__developer.name = developer_data.get('name')
        self.__developer.premium = developer_data.get('premium')
        self.__developer.region = developer_data.get('region')
        self.__developer.role = "developer"
        self.__developer.contact_number = developer_data.get('contact_number')
    
        if not self.__user_service.verify_password(upasswordhash.encode('utf-8'), developer_data.get('password')):
            return {"success": False, "message": "Invalid email or password", "user": None}

        new_uuid = uuid.uuid4()
        self.__developer.api_key = str(new_uuid)
        self.__driver.update_document('users', developer_data.get("doc_id"), self.__developer.to_dict())
        
    
    def save_request(self, api_key):
        if api_key:
            developer_data = self.__driver.find_by_parameter("users", {"api_key": api_key})
            if not developer_data:
                return False
            developer_data = developer_data[0]
            for key, value in developer_data.items():
                if hasattr(self.__developer, key):
                    setattr(self.__developer, key, value)
            print(self.__developer)
            dev_doc = developer_data["doc_id"]
            self.__driver.create_document("requests", {"dev_doc_id": dev_doc, "time-stamp": int(time.time())})
            return True
        return False
    
    def get_requests(self, email):
        if email:
            developer_data = self.__driver.find_by_parameter("users", {"email": email})
            if not developer_data:
                return {"success": False, "Message": "user not found"}
            developer_data = developer_data[0]
            for key, value in developer_data.items():
                if hasattr(self.__developer, key):
                    setattr(self.__developer, key, value)
            dev_doc = developer_data["doc_id"]
            reqs = self.__driver.find_by_parameter("requests", {"dev_doc_id": dev_doc})
            
            human_readable_timestamps = []
            int_timestamps = []

            for req in reqs:
                timestamp = req["time-stamp"]
                human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
                human_readable_timestamps.append(human_readable_time)
                int_timestamps.append(timestamp)

            return {"success": True, "human_readable_timestamps": human_readable_timestamps, "int_timestamps": int_timestamps, "req_count": len(int_timestamps), "total_usage": self.__developer.quota}
    
            

        return {"success": False, "message": "email should not be empty"}    