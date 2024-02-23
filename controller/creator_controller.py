from flask import Flask, Blueprint

creator_controller = Blueprint('creator_controller', __name__)

@creator_controller.route('/', methods=['GET'])
def get_success_message():
    return "retrieve all creator details"
