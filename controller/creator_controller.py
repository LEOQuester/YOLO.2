from flask import jsonify, Blueprint, request
from data.creator import Creator
from data.boost import Boost
from service.creator_service import CreatorService
from flask_cors import CORS

creator_controller = Blueprint('creator_controller', __name__)
CORS(creator_controller)


class CreatorController():
    __creator_service = CreatorService()

    @staticmethod
    @creator_controller.route('/', methods=['GET'])
    def get_all_creators():
        return jsonify(CreatorController.__creator_service.get_all_creators())

    @staticmethod
    @creator_controller.route('/pending', methods=['GET'])
    def get_pending_requests():
        return jsonify(CreatorController.__creator_service.get_pending_requests())

    @staticmethod
    @creator_controller.route('/request', methods=['POST'])
    def signup_for_creator():
        data = request.json
        response = CreatorController.__creator_service.signup_for_creator(data["email"], data['type'], data['link'],
                                                                          data['business_email'], data['description']   )
        if response["success"]:
            return response, 200
        else:
            return response, 

    @staticmethod
    @creator_controller.route('/boost', methods=['POST'])
    def save_boost():
       return CreatorController.__creator_service.save_boost()
