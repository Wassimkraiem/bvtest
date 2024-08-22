from sev.dynamodb import video_table



def upload_video(item): 
    video = video_table.upload_video(item)
    

def get_video_by_id(video_id):
    return video_table.get_video(video_id)

def delete_video(video_id):
    return video_table.delete_item(video_id)