# sev/views/search_view.py
from flask import Blueprint, jsonify
from sev.apps.videos.opensearch.resources import SearchResource
from flask import request
from flask_restful import Api
from flask_restful import Resource



blueprint = Blueprint("videos_opensearch",__name__,url_prefix="/")
api = Api(blueprint)

api.add_resource(SearchResource,"/videosopensearch")