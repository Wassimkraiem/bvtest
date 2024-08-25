from flask import Flask
from sev.dynamodb import initialize_dynamodb
from sev.dynamodb import list_dynamodb_tables
from sev.apps.videos.dynamo.views import blueprint as videos_blueprint
#from sev.apps.videos.opensearch.views import blueprint as videos_opensearch
from sev.opensearch import create_opensearch_client

def register_blueprint(app):
    app.register_blueprint(videos_blueprint)
    #app.register_blueprint(videos_opensearch)

def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    initialize_dynamodb(app)
    list_dynamodb_tables(app)
    #create_opensearch_client(app)
    return app
bviral_app = create_app()