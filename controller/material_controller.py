from flask import Blueprint, request, jsonify
from model.engineAI import Engine
from service.material_service import Material
from repo.firebaseConfig import db

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
    

    # public endpoint need a dynamic api key assiging and validation for developer role unlocked users
    @material_controller.route('/api/media', methods=[
        'GET'])  # example request : http://localhost:5000/api/media?title=TITLE_OF_THE_CONTENT&media_type=MEDIA&api_key=JSHBKSDBKSDCNJNSKJNJSKNAKJNAK (movie,tv, anime_movie, anime_tv, song, book)
    def get_media():
        # Get parameters from the query string
        title = request.args.get('title', default='', type=str)
        media_type = request.args.get('media_type', default='', type=str)
        api_key = request.args.get('api_key', default='', type=str)

        if not title or not media_type or not api_key:
            return jsonify({"error": "Both 'title' and 'media_type' and api_key parameters are required."}), 400
        query = db.collection('users').where('api_key', '==', api_key).limit(1).get()
        if not query:
            return jsonify({'error': 'invalid api Key or key not exist'}), 404

        count = query[0].to_dict()['request_count']
        query[0].reference.set({
            'request_count' : count + 1
        }, merge = True)
        material = Material()
        if media_type == "movie" or media_type == "tv":
            result = material.media_from_title(title=title, media_type=media_type)
        elif media_type == "song":
            return jsonify(material.get_songs([title], media_type))
        elif media_type == "book":
            return jsonify(material.get_books([title]))
        elif media_type == "anime_movie":
            return jsonify(material.get_anime([title], 'movie'))
        elif media_type == "anime_tv":
            return jsonify(material.get_anime([title], 'tv'))
        else:
            return jsonify({"error": "Media_type invalid"}), 400

        if result is not None:
            return jsonify(result)
        else:
            return jsonify({"error": "An error occurred while fetching media data."}), 500
