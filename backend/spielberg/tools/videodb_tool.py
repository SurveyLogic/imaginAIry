import os

import videodb

from videodb.timeline import Timeline
from videodb.asset import VideoAsset, ImageAsset


class VideoDBTool:
    def __init__(self, collection_id="default"):
        self.conn = videodb.connect(
            base_url=os.getenv("VIDEO_DB_BASE_URL", "https://api.videodb.io")
        )
        self.collection = None
        if collection_id:
            self.collection = self.conn.get_collection(collection_id)
        self.timeline = None

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

    def get_transcript(self, video_id: str, text=True):
        video = self.collection.get_video(video_id)
        if text:
            transcript = video.get_transcript_text()
        else:
            transcript = video.get_transcript()
        return transcript

    def index_spoken_words(self, video_id: str):
        # TODO: Language support
        video = self.collection.get_video(video_id)
        index = video.index_spoken_words()
        return index

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

    def add_brandkit(self, video_id, intro_video_id, outro_video_id, brand_image_id):
        timeline = Timeline(self.conn)
        if intro_video_id:
            intro_video = VideoAsset(asset_id=intro_video_id)
            timeline.add_inline(intro_video)
        video = VideoAsset(asset_id=video_id)
        timeline.add_inline(video)
        if outro_video_id:
            outro_video = VideoAsset(asset_id=outro_video_id)
            timeline.add_inline(outro_video)
        if brand_image_id:
            brand_image = ImageAsset(asset_id=brand_image_id)
            timeline.add_overlay(0, brand_image)
        stream_url = timeline.generate_stream()
        return stream_url

    def get_and_set_timeline(self):
        self.timeline = Timeline(self.conn)
        return self.timeline
