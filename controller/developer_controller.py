from flask import Blueprint, request
from service.developer_service import DeveloperService

developer_controller = Blueprint('developer_controller', __name__)

class DeveloperController():
    __developer_service = DeveloperService()
    
    @staticmethod
    @developer_controller.route('/create', methods=["POST"])
    def unlock_developer():
        data = request.json
        result = DeveloperController.__developer_service.createDeveloper(data["email"], data["password"])
        return result  
