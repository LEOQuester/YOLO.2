from repo.FirebaseDriver import FirebaseDriver
from data.user import User
import bcrypt
class UserService():

    def __init__(self):
        self.__driver =  FirebaseDriver()

    def createUser(self, user: User):
        users = self.__driver.find_by_parameter("users", {"email": user.email})
        if  users:
            return {"success": False}
        user.password = self.__hash_password(user.password)
        user_dict = user.to_dict()
        operation = self.__driver.create_document('users', user_dict)
        return {"success": True}

    def login_user(self, email, password):
        users = self.__driver.find_by_parameter("users", {"email": email})
        if not users:
            return {"success": False, "message": "User not found", "user": None}
        user = users[0]
        if not self.verify_password(password.encode('utf-8'), user['password']):
            return {"success": False, "message": "Invalid email or password", "user": None}
        else:
            # Decode the password from bytes to string
            user['password'] = user['password'].decode('utf-8')
            return user

    def getAllUsers(self, email):
        users = self.__driver.find_by_parameter("test", {"email": email})

        # Filter out non-JSON serializable data (e.g., bytes)
        filtered_users = []
        for user in users:
            filtered_user = {}
            for key, value in user.items():
                if isinstance(value, bytes):
                    continue  # Omit bytes values
                filtered_user[key] = value
            filtered_users.append(filtered_user)

        return filtered_users
    
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password, hashed_password)

    def __hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password