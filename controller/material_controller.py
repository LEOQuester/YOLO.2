from flask import Blueprint, request, jsonify
from model.engineAI import Engine
from service.developer_service import DeveloperService
from service.material_service import Material
from flask_cors import CORS


#TODO: BAD OUTPUT, CHECK THE RESPONSES, SENDS SAME EVERYTIME
material_controller = Blueprint('material_controller', __name__)
CORS(material_controller)

@material_controller.route('/', methods=['GET'])
def get_success_message():
    return "all the materials"

class MaterialController():

    #IMPORTANT: ONLY categorize ENDPOINT IS ACCESSIBLE FOR THE DEVELOPERS
    __developer_Service = DeveloperService()
    __material = Material()
    # Spotify API endpoints
    SPOTIFY_API_URL = 'https://api.spotify.com/v1/'

    # OAuth2 Authorization URLs
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'



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
        return jsonify(response), 200

    @staticmethod
    @material_controller.route('/categorize', methods=['POST'])
    def categorize():
        # get the token from the request and check the user services for the token. update the token's usage count
        if not request.json:
            return jsonify({'error': 'request must contain JSON data'}), 400
        data = request.json
        try:
            prompt = data['prompt']
            token = data['token']
        except KeyError:
            return jsonify({'error': 'prompt or token is missing'}), 400
        
        if not prompt:
            return jsonify({'error': 'prompt is empty'}), 400
        
        engine = Engine()

        if MaterialController.__developer_Service.save_request(token) == False:
            return jsonify({"error": "api did not accept"}), 400
            
        response = engine.query(prompt)
        return jsonify({"success":True, "labels": response}), 200
    
            
    @staticmethod
    @material_controller.route('/tv', methods=[
        'GET'])  # example request : http://localhost:5000/movies?keywords=marvel,adventure&media_type=movie (movie / tv)
    def get_movies():
        keywords_param = request.args.get('keywords')
        keywords = keywords_param.split(',') if keywords_param else []
        media_type = request.args.get('media_type')
        return jsonify(MaterialController.__material.media_from_keywords(keywords, media_type))




    @staticmethod
    @material_controller.route('/songs', methods=[
        'GET'])  # example request : http://localhost:5000/songs?keywords=marvel,adventure&media_type=song (song / video)
    def get_audio():
        keywords_string = request.args.get('keywords', default='', type=str)
        media_type = request.args.get('media_type', default='', type=str)
        keywords_array = keywords_string.split(',')
        result = MaterialController.__material.get_songs(keywords_array, media_type)
        return jsonify(result)



    @staticmethod
    @material_controller.route('/books', methods=['GET'])  # example request : http://localhost:5000/books?keywords=marvel,adventure
    def get_reads():
        keywords_string = request.args.get('keywords', default='', type=str)
        keywords_array = keywords_string.split(',')
        print(keywords_array)
        return jsonify(MaterialController.__material.get_books(keywords_array))

    @staticmethod
    @material_controller.route('/anime', methods=[
        'GET'])  # example request : http://localhost:5000/anime?keywords=marvel,adventure&media_type=movie (movie / tv)
    def get_animes():
        keywords_string = request.args.get('keywords', default='', type=str)
        media_type = request.args.get('media_type', default='', type=str)
        keywords_array = keywords_string.split(',')
        return MaterialController.__material.get_anime(keywords_array, media_type)
    
    # @staticmethod
    # @material_controller.route('/categorize', methods=[
    #     'POST']) 
    # def get_keywords():
    #     data = request.json
    #     return MaterialController.__developer_Service.getKeyList(data['prompt'])
    

    # public endpoint need a dynamic api key assiging and validation for developer role unlocked users
    @staticmethod
    @material_controller.route('/media', methods=[
        'GET'])  # example request : http://localhost:5000/api/media?title=TITLE_OF_THE_CONTENT&media_type=MEDIA&api_key=JSHBKSDBKSDCNJNSKJNJSKNAKJNAK (movie,tv, anime_movie, anime_tv, song, book)
    def get_media():
        # Get parameters from the query string
        title = request.args.get('title', default='', type=str)
        media_type = request.args.get('media_type', default='', type=str)
        api_key = request.args.get('api_key', default='', type=str)

        if MaterialController.__developer_Service.save_request(api_key) == False:
            return jsonify({"error": "api did not accept"}), 400

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
    
    
    @staticmethod
    @material_controller.route('/keywords', methods=['GET'])
    def get_all_keywords():
        engine = Engine()
        return engine.get_all_keywords()
