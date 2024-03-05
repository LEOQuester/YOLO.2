from flask import jsonify, Blueprint, request
from data.user import User
from service.user_service import UserService
from flask_cors import CORS
user_controller = Blueprint('user_controller', __name__)
CORS(user_controller)

class UserController():
    __user_service = UserService()
    
    @staticmethod
    @user_controller.route('/register', methods=["POST"])
    def create_user():
        data = request.json
        if 'password' in data:
            data['password'] = data['password'].encode()
        user = User(**data)
        response = UserController.__user_service.createUser(user)
        if response["success"]:
            return response, 200
        else:
            return response, 400

    @staticmethod
    @user_controller.route('/login', methods=["POST"])
    def login_users():
        data = request.json
        response =  UserController.__user_service.login_user(data["email"], data["password"])
        if response:
            return response, 200
        else:
            return jsonify({"error": "user not found", "success": False}), 400
    
    @staticmethod
    @user_controller.route('/', methods=["GET"])
    def get_users():
        print(request.args.get("email"))
        return UserController.__user_service.getAllUsers(request.args.get("email")), 200


    @staticmethod
    @user_controller.route('/premium', methods=["POST"])
    def premium_user():
       #TODO
        pass