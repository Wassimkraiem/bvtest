from flask import request
from flask_restful import Resource
from sev.dynamodb import video_table
from sev.apps.videos.dynamo.services import get_video_by_id
from sev.apps.videos.dynamo.services import upload_video
from sev.apps.videos.dynamo.services import delete_video

class VideoList(Resource):
    def get(self):
        video_id = request.args.get('video_id')
        return get_video_by_id(video_id)

    def post(self):
        video_data = request.get_json()
        upload_video(video_data)
        return {"message": "Video uploaded successfully"}, 200
    
    def delete(self):
        video_id = request.args.get('videoId')
        delete_video(video_id)
        return {"message": "Video deleted successfully"}, 200