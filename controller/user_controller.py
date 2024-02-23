from flask import jsonify, Blueprint, request
from data.user import User
from service.user_service import UserService

user_controller = Blueprint('user_controller', __name__)

class UserController():
    
    @staticmethod
    @user_controller.route('/', methods=["POST"])
    def create_user():
        data = request.json
        user = User(**data)
        service = UserService()
        return jsonify(service.createUser(user))
    
    @staticmethod
    @user_controller.route('/login', methods=["POST"])
    def login_users():
        data = request.json
        service = UserService()
        return service.login_user(data["email"], data["password"])
    
    @staticmethod
    @user_controller.route('/', methods=["GET"])
    def get_users():
        service = UserService()
        print(request.args.get("email"))
        return service.getAllUsers(request.args.get("email"))


