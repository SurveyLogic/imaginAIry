import logging

import yt_dlp

from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus
from spielberg.core.session import Session, MsgStatus, VideoContent, TextContent
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

UPLOAD_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "description": "URL to upload the content",
        },
        "media_type": {
            "type": "string",
            "enum": ["video", "audio", "image"],
            "description": "Type of media to upload, default is video",
        },
        "collection_id": {
            "type": "string",
            "description": "Collection ID to upload the content",
        },
    },
    "required": ["url", "media_type"],
}


class UploadAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "upload"
        self.description = "Uploads media content to the VideoDB. This agent takes a URL of the media content and uploads it to the VideoDB. The media content can be a video, audio, or image file. Youtube playlist and links are also supported."
        self.parameters = UPLOAD_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def _upload(self, url: str, media_type: str):
        """Upload the media with the given URL."""
        try:
            if media_type == "video":
                content = VideoContent(
                    agent_name=self.agent_name, status=MsgStatus.progress
                )
            else:
                content = TextContent(
                    agent_name=self.agent_name, status=MsgStatus.progress
                )
            self.output_message.content.append(content)
            content.status_message = f"Uploading {media_type}..."
            self.output_message.push_update()

            upload_data = self.videodb_tool.upload(url, media_type)

            content.status_message = f"{upload_data['name']} uploaded successfully"
            if media_type == "video":
                content.video = upload_data
            else:
                content.text = (
                    f"\n ID: {upload_data['id']}, TITLE: {upload_data['name']}"
                )
            content.status = MsgStatus.success
            return upload_data

        except Exception as e:
            logger.exception(f"error in {self.agent_name} agent: {e}")
            content.status = MsgStatus.error
            content.status_message = f"Error in uploading {media_type}"
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

    def _get_yt_playlist_videos(self, playlist_url: str):
        """Get the list of videos from a youtube playlist."""
        try:
            # Create the downloader object
            with yt_dlp.YoutubeDL({"extract_flat": True, "quiet": True}) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
            if "entries" in playlist_info:
                video_list = []
                for video in playlist_info["entries"]:
                    video_list.append(
                        {
                            "title": video.get("title", "Unknown Title"),
                            "url": f"https://www.youtube.com/watch?v={video['id']}",
                        }
                    )
                return video_list
        except Exception as e:
            logger.exception(f"Error in getting playlist info: {e}")
            return None

    def _upload_yt_playlist(self, playlist_info: dict, media_type):
        """Upload the videos in a youtube playlist."""
        try:
            for media in playlist_info:
                self.output_message.actions.append(
                    f"Uploading video: {media['title']} as {media_type}"
                )
                self._upload(media["url"], media_type)
        except Exception as e:
            logger.exception(f"Error in uploading playlist: {e}")
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="All the videos in the playlist uploaded successfully as {media_type}",
        )

    def run(
        self, url: str, media_type="video", collection_id: str = None, *args, **kwargs
    ) -> AgentResponse:
        """
        Upload the media with the given URL.

        :param url: The URL of the media to upload.
        :type url: str
        :param media_type: The type of media to upload, defaults to "video"
        :type media_type: str, optional
        :return: The response containing information about the upload operation.
        :rtype: AgentResponse
        """

        if collection_id is None:
            self.videodb_tool = VideoDBTool()
        else:
            self.videodb_tool = VideoDBTool(collection_id=collection_id)

        # check if the url is a youtube playlist
        playlist_info = self._get_yt_playlist_videos(url)
        if playlist_info:
            self.output_message.actions.append("Youtube playlist detected")
            self.output_message.push_update()
            return self._upload_yt_playlist(playlist_info, media_type)

        # upload the media
        upload_data = self._upload(url, media_type)
        self.output_message.publish()

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="Upload successful",
            data=upload_data,
        )
