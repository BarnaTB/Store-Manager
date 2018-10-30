from api.views import blueprint
from flask import Flask


app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix='/api/v1')
