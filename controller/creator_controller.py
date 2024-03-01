from flask import jsonify, Blueprint, request
from data.creator import Creator
from data.boost import Boost
from service.creator_service import CreatorService
from flask_cors import CORS

creator_controller = Blueprint('creator_controller', __name__)
CORS(creator_controller)

class CreatorController():
    __creator_service = CreatorService()

@creator_controller.route('/', methods=['POST'])
def update_creator():
    data = request.json
    CreatorController.__creator_service.update_to_creator(data["email"], data["phone"], data["sm_links"])
