from repo.FirebaseDriver import FirebaseDriver
from data.admin import Admin
import bcrypt
class AdminService():

    def __init__(self):
        self.__driver =  FirebaseDriver()

    def create_admin(self, admin: Admin):
        users = self.__driver.find_by_parameter("admin", {"email": admin.email})
        if  users:
            return {"success": False, "message": "admin already exist", "user": None}
        admin.password = self.__hash_password(admin.password)
        operation = self.__driver.create_document('admin', admin.to_dict())
        return operation['doc_id']
    
    def login_admin(self, email, password):
        admins = self.__driver.find_by_parameter("admin", {"email": email})
        if not admins:
            return {"success": False, "message": "admin not found", "user": None}
        admin = admins[0]
        if not self.verify_password(password.encode('utf-8'), admin['password']):
            return {"success": False, "message": "Invalid email or password", "user": None}
        else:
            key = admin['password'].decode('utf-8')
            return {"success": True, "message": "Login successful", "admin": admin['name'], "email": admin['email'], "password": key}
    
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password, hashed_password)

    def __hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password