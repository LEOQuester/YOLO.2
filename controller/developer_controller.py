from flask import Flask, Blueprint

developer_controller = Blueprint('developer_controller', __name__)

@developer_controller.route('/', methods=['GET'])
def get_success_message():
    return "retrieve all developer details"
