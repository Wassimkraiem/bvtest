
from opensearchpy import OpenSearch

class VideoOpensearch:
    def __init__(self, client):
        self.client = client

    def index_video(self, video_data):
        response = self.client.index(
            index='videos',
            body=video_data,
            refresh=True
        )
        return response

    def search_videos(self, query):
        query_body = {
            "query": {
                "match": {
                    "title": query  
                }
            }
        }
        response = self.client.search(
            index='videos',
            body=query_body
        )
        return response

def create_opensearch_client(app=None):
    client = OpenSearch(
        hosts=[{'host': 'localhost', 'port': 9200}],
        http_auth=('admin', 'Wassim123*'), 
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    video_opensearch = VideoOpensearch(client)

    if app:
        app.extensions['video_opensearch'] = video_opensearch
    
    return video_opensearch
