# sev/services/search_service.py
from flask import current_app

class SearchService:
    def __init__(self, video_opensearch):
        self.video_opensearch = video_opensearch

    def index_video(self, video_data):
        response = self.video_opensearch.index_video(video_data)
        return response

    def search_videos(self, query):
        response = self.video_opensearch.search_videos(query)
        return response
