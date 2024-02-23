from flask import Flask, Blueprint

admin_controller = Blueprint('admin_controller', __name__)

@admin_controller.route('/', methods=['GET'])
def get_success_message():
    return "all the admins"
