from flask import Flask, Blueprint

payment_controller = Blueprint('payment_controller', __name__)

@payment_controller.route('/', methods=['GET'])
def get_success_message():
    return "all the payments"
