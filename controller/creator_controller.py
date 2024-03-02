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
    @creator_controller.route('/', methods=['POST'])
    def update_creator():
        data = request.json
        return jsonify(
            CreatorController.__creator_service.update_to_creator(data["email"], data["phone"], data["sm_links"]))

    @staticmethod
    @creator_controller.route('/', methods=['GET'])
    def get_all_creators():
        return jsonify(CreatorController.__creator_service.get_all_creators())

    @staticmethod
    @creator_controller.route('/request', methods=['POST'])
    def request_application():
        data = request.json
        response = CreatorController.__creator_service.add_request(data["email"], data['type'], data['link'],
                                                                   data['business_email'], data['description'])
        if response["success"]:
            return response, 200
        else:
            return response, 400
