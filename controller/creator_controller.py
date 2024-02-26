from flask import Blueprint

creator_controller = Blueprint('creator_controller', __name__)

@creator_controller.route('/', methods=['GET'])
def save_collection():
    return "retrieve all creator details"
