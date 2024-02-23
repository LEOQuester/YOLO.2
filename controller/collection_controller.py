from flask import Flask, Blueprint

collection_controller = Blueprint('collection_controller', __name__)

@collection_controller.route('/', methods=['GET'])
def get_success_message():
    return "all the collections"
