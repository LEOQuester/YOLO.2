from flask import Flask, Blueprint, request, jsonify
from model.engineAI import Engine
from service.material_service import Material

material_controller = Blueprint('material_controller', __name__)

@material_controller.route('/', methods=['GET'])
def get_success_message():
    return "all the materials"

class MaterialController():

    @staticmethod
    @material_controller.route("/keywords", methods=["POST"])
    def get_keywords():
        if not request.is_json:
            return jsonify({'error': 'request must contain JSON data'}), 400

        try:
            prompt = request.get_json()['prompt']
        except KeyError:
            return jsonify({'error': 'prompt is missing'}), 400
        
        if not prompt:
            return jsonify({'error': 'prompt is empty'}), 400
        
        engine = Engine()
        response = engine.query(prompt)
        return jsonify(response)

        
    @material_controller.route('/movies', methods=[
        'GET'])  # example request : http://localhost:5000/movies?keywords=marvel,adventure&media_type=movie (movie / tv)
    def get_movies():
        keywords_param = request.args.get('keywords')
        keywords = keywords_param.split(',') if keywords_param else []
        media_type = request.args.get('media_type')
        material = Material()
        return jsonify(material.media_from_keywords(keywords, media_type))


    @material_controller.route('/songs', methods=[
        'GET'])  # example request : http://localhost:5000/songs?keywords=marvel,adventure&media_type=song (song / video)
    def get_audio():
        keywords_string = request.args.get('keywords', default='', type=str)
        media_type = request.args.get('media_type', default='', type=str)
        keywords_array = keywords_string.split(',')
        material = Material()
        result = material.get_songs(keywords_array, media_type)
        return jsonify(result)


    @material_controller.route('/books', methods=['GET'])  # example request : http://localhost:5000/books?keywords=marvel,adventure
    def get_reads():
        keywords_string = request.args.get('keywords', default='', type=str)
        keywords_array = keywords_string.split(',')
        material = Material()
        return jsonify(material.get_books(keywords_array))


    @material_controller.route('/anime', methods=[
        'GET'])  # example request : http://localhost:5000/anime?keywords=marvel,adventure&media_type=movie (movie / tv)
    def get_animes():
        keywords_string = request.args.get('keywords', default='', type=str)
        media_type = request.args.get('media_type', default='', type=str)
        keywords_array = keywords_string.split(',')
        material = Material()
        return material.get_anime(keywords_array, media_type)
