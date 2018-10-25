from api.views import blueprint
from flask import Flask
from flask_jwt_extended import JWTManager


app = Flask(__name__)
JWTManager(app)

app.register_blueprint(blueprint, url_prefix='/api/v1')
