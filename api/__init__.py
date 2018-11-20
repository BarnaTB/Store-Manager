from api.views import blueprint
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)

JWTManager(app)
Swagger(app)
CORS(app)
app.register_blueprint(blueprint, url_prefix='/api/v1')
app.config['JWT_SECRET_KEY'] = 'you-dont-know-whats-here'
