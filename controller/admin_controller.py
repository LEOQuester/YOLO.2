from flask import jsonify, Blueprint, request
from data.admin import Admin
from service.admin_service import AdminService
from flask_cors import CORS

admin_controller = Blueprint('admin_controller', __name__)
CORS(admin_controller)

class AdminController():
    __admin_service = AdminService()
        
    @staticmethod
    @admin_controller.route('/', methods=["POST"])
    def create_admin():
        data = request.json
        if not data.get("permission_key") or data["permission_key"] != "YOLO_SECURITY_CODE_718627836":
            return "access denied!"

        if 'password' in data:
            data['password'] = data['password'].encode()
        admin = Admin(email=data["email"], password=data["password"], name=data["name"])
        return jsonify(AdminController.__admin_service.create_admin(admin))
    
    @staticmethod
    @admin_controller.route('/login', methods=["POST"])
    def login_users():
        data = request.json
        response = AdminController.__admin_service.login_admin(data["email"], data["password"])
        if response["success"]:
            return response, 200
        else:
            return response, 400

