from flask import Blueprint, request
from service.developer_service import DeveloperService
from flask_cors import CORS

developer_controller = Blueprint('developer_controller', __name__)
CORS(developer_controller)

class DeveloperController():
    __developer_service = DeveloperService()

    
    
    @staticmethod
    @developer_controller.route('/create', methods=["POST"])
    def unlock_developer():
        data = request.json
        result = DeveloperController.__developer_service.createDeveloper(data["email"], data["password"])
        return result  
    
    @staticmethod
    @developer_controller.route('/usage', methods=['GET'])
    def get_usage():
        email = request.args.get('email', default='', type=str)
        return DeveloperController.__developer_service.get_requests(email)

    @staticmethod
    @developer_controller.route('/generate', methods=['GET'])
    def generate_token():
        #TODO
        pass

    @staticmethod
    @developer_controller.route('/usage', methods=['GET'])
    def fetch_all():
        #TODO
        pass

