from flask import request, current_app
from flask_restful import Resource
from sev.apps.videos.opensearch.services import SearchService


class SearchResource(Resource):
    def __init__(self):
        # Access video_opensearch from current_app.extensions
        video_opensearch = current_app.extensions.get('video_opensearch')
        if video_opensearch is None:
            raise RuntimeError("OpenSearch client not found in app extensions.")
        self.search_service = SearchService(video_opensearch)

    def post(self):
        video_data = request.json
        response = self.search_service.index_video(video_data)
        return response

    def get(self):
        query = request.args.get('query', '')
        response = self.search_service.search_videos(query)
        return response
