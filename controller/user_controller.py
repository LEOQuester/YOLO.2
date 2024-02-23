from flask import Flask, Blueprint



user_controller = Blueprint('user_controller', __name__)

# @user_controller.route('/', methods=['GET'])
# def get_success_message():
#     return "retrieve all user details"


class UserController():

    @staticmethod
    @user_controller.route('/')
    def index():
        return "hello world"
