#import basics
from flask import Flask
from flask_cors import CORS


#import packages
from controller.user_controller import user_controller
from controller.developer_controller import developer_controller
from controller.creator_controller import creator_controller
from controller.material_controller import material_controller
from controller.collection_controller import collection_controller
from controller.payment_controller import payment_controller
from controller.admin_controller import admin_controller

app = Flask(__name__)
app.register_blueprint(user_controller, url_prefix = "/users")
app.register_blueprint(developer_controller, url_prefix = "/developers")
app.register_blueprint(admin_controller, url_prefix = "/admin")
app.register_blueprint(creator_controller, url_prefix = "/creators")
app.register_blueprint(material_controller, url_prefix = "/materials")
app.register_blueprint(collection_controller, url_prefix = "/collections")
app.register_blueprint(payment_controller, url_prefix = "/payment")

CORS(app)

if __name__ == '__main__':
    app.run(debug=True)