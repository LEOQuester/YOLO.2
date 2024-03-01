from flask import jsonify, Blueprint, request
from data.collection import Collection
from service.collection_service import CollectionService
from flask_cors import CORS

collection_controller = Blueprint('collection_controller', __name__)
CORS(collection_controller)

class CollectionController():
    __collection_service = CollectionService()
    
    @staticmethod
    @collection_controller.route('/', methods=["POST"])
    def create_collection():
        data = request.json
        collection = Collection(**data)
        return jsonify(CollectionController.__collection_service.create_collection(collection))
    
    @staticmethod
    @collection_controller.route('/', methods=["GET"])
    def all_collections():
         return jsonify(CollectionController.__collection_service.get_all_collections())

