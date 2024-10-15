import os
from videodb import connect, SearchType


class VideoDBTool:
    def __init__(self, collection_id="default"):
        self.conn = connect(
            base_url=os.getenv("VIDEO_DB_BASE_URL", "https://api.videodb.io")
        )
        if collection_id:
            self.collection = self.conn.get_collection(collection_id)

    def get_collection(self):
        return {
            "id": self.collection.id,
            "name": self.collection.name,
            "description": self.collection.description,
        }

    def get_collections(self):
        """Get all collections."""
        collections = self.conn.get_collections()
        return [
            {
                "id": collection.id,
                "name": collection.name,
                "description": collection.description,
            }
            for collection in collections
        ]

    def get_video(self, video_id):
        """Get a video by ID."""
        video = self.collection.get_video(video_id)
        return {
            "id": video.id,
            "name": video.name,
            "description": video.description,
            "collection_id": video.collection_id,
            "stream_url": video.stream_url,
            "length": video.length,
            "thumbnail_url": video.thumbnail_url,
        }

    def get_videos(self):
        """Get all videos in a collection."""
        videos = self.collection.get_videos()
        return [
            {
                "id": video.id,
                "name": video.name,
                "description": video.description,
                "collection_id": video.collection_id,
                "stream_url": video.stream_url,
                "length": video.length,
                "thumbnail_url": video.thumbnail_url,
            }
            for video in videos
        ]

    def upload(self, url):
        media = self.collection.upload(url=url)
        return {
            "id": media.id,
            "collection_id": media.collection_id,
            "stream_url": media.stream_url,
            "player_url": media.player_url,
            "name": media.name,
            "description": media.description,
            "thumbnail_url": media.thumbnail_url,
            "length": media.length,
        }

    def generate_thumbnail(self, video_id: str, timestamp: int = 5):
        video = self.collection.get_video(video_id)
        image = video.generate_thumbnail(time=float(timestamp))
        return {
            "id": image.id,
            "collection_id": image.collection_id,
            "name": image.name,
            "url": image.url,
        }

    def get_transcript(self, video_id: str):
        # TODO: Flag for just text
        video = self.collection.get_video(video_id)
        transcript = video.get_transcript_text()
        return transcript

    def index_spoken_words(self, video_id: str):
        # TODO: Language support
        video = self.collection.get_video(video_id)
        index = video.index_spoken_words()
        return index

    def index_scene(self, video_id: str):
        video = self.collection.get_video(video_id)
        return video.index_scenes()

    def download(self, stream_link: str, name: str = None):
        download_response = self.conn.download(stream_link, name)
        return download_response

    def semantic_search(self, query, video_id=None):
        if video_id:
            video = self.collection.get_video(video_id)
            search_resuls = video.search(query=query)
        else:
            search_resuls = self.collection.search(query=query)
        return search_resuls

    def keyword_search(self, query, video_id=None):
        """Search for a keyword in a video."""
        video = self.collection.get_video(video_id)
        return video.search(query=query, search_type=SearchType.keyword)

    def generate_video_stream(self, video_id: str, timeline):
        """Generate a video stream from a timeline. timeline is a list of tuples. ex [(0, 10), (20, 30)]"""
        video = self.collection.get_video(video_id)
        return video.generate_stream(timeline)
