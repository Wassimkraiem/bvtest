from flask import Flask
from sev.dynamodb import initialize_dynamodb
from sev.apps.videos.views import blueprint as videos_blueprint


def register_blueprint(app):
    app.register_blueprint(videos_blueprint)

def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    initialize_dynamodb(app)
    return app
bviral_app = create_app()