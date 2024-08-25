from flask import Blueprint
from flask import request
from flask_restful import Api
from flask_restful import Resource
from sev.apps.videos.dynamo.resources import VideoList


blueprint = Blueprint("videos_blueprint",__name__,url_prefix="/")
api = Api(blueprint)

api.add_resource(VideoList,"/videos/<int:video_id>")