from flask import Flask

from .routes import messenger
from .routes import static

api = Flask(__name__)

api.register_blueprint(messenger)
api.register_blueprint(static)
