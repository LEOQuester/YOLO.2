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
    @creator_controller.route('/approved', methods=['GET'])
    def get_approved_requests_by_email():
        email = request.args.get("email")
        return jsonify(CreatorController.__creator_service.get_approved_reqeusts_for_cc(email))

    @staticmethod
    @creator_controller.route('/paid', methods=['GET'])
    def get_paid_request_by_email():
        email = request.args.get("email")
        return jsonify(CreatorController.__creator_service.get_paid_requests_for_cc(email))

    @staticmethod
    @creator_controller.route('/request', methods=['POST'])
    def signup_for_creator():
        data = request.json
        response = CreatorController.__creator_service.signup_for_creator(data["email"], data['type'], data['link'],
                                                                          data['business_email'], data['description'])
        if response["success"]:
            return response, 200
        else:
            return response, 400


    @staticmethod
    @creator_controller.route('/boost', methods=['POST'])
    def request_boost():
        data = request.json
        return jsonify(CreatorController.__creator_service.place_boost_request(data["email"], data["title"], data["content_url"], data["keywords"]))

    @staticmethod
    @creator_controller.route('/approve', methods=['GET'])
    def approve_boost():
        doc = request.args.get("doc")
        print(doc)
        return  jsonify({"success": True, "message": "Boost approved"}) if CreatorController.__creator_service.approve_boost(doc) else jsonify({"success": False, "message": "Boost failed to approve"})

    @staticmethod
    @creator_controller.route('/reject', methods=['GET'])
    def reject_boost():
        doc = request.args.get("doc")
        return jsonify({"success": True, "message": "Boost rejected"}) if CreatorControler.__creator_service.reject_boost(doc) else jsonify({"success": False, "message": "Boost failed to reject"})

    @staticmethod
    @creator_controller.route('/approve_payment', methods=['GET'])
    def approve_payment():
        doc = request.args.get("doc")
        return jsonify({"success": True, "message": "Payment approved"}) if CreatorController.__creator_service.approve_payment(doc) else jsonify({"success": False, "message": "Payment failed to approve"})