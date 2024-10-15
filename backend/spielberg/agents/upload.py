import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult

from spielberg.core.session import Session, MsgStatus, VideoContent
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

UPLOAD_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "description": "URL to upload the content",
        },
        "collection_id": {
            "type": "string",
            "description": "Collection ID to upload the content",
        },
    },
    "required": ["url"],
}


class UploadAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "upload"
        self.description = "Use this Agent to upload the media with the given url."
        self.parameters = UPLOAD_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def __call__(
        self, url: str, collection_id: str = None, *args, **kwargs
    ) -> AgentResponse:
        """
        Upload the media with the given URL.

        :param url: The URL of the media to upload.
        :type url: str
        :return: The response containing information about the upload operation.
        :rtype: AgentResponse
        """
        try:
            video_content = VideoContent(
                agent_name=self.agent_name, status=MsgStatus.progress
            )
            self.output_message.content.append(video_content)
            video_content.status_message = "Uploading video.."
            self.output_message.push_update()

            if collection_id is None:
                videodb_tool = VideoDBTool()
            else:
                videodb_tool = VideoDBTool(collection_id=collection_id)
            upload_data = videodb_tool.upload(url)
            video_content.status_message = "Video uploaded successfully"
            video_content.video = {
                "id": upload_data["id"],
                "collection_id": upload_data["collection_id"],
                "stream_url": upload_data["stream_url"],
                "player_url": upload_data["player_url"],
                "name": upload_data["name"],
                "description": upload_data["description"],
                "thumbnail_url": upload_data["thumbnail_url"],
                "length": upload_data["length"],
            }
            video_content.status = MsgStatus.success
            self.output_message.publish()

        except Exception as e:
            logger.exception(f"error in {self.agent_name} agent: {e}")
            video_content.status = MsgStatus.error
            video_content.status_message = "Error in uploading video."
            self.output_message.publish()
            return AgentResponse(result=AgentResult.ERROR, message=str(e))

        return AgentResponse(
            result=AgentResult.SUCCESS,
            message="Upload successful",
            data={
                "id": upload_data["id"],
                "collection_id": upload_data["collection_id"],
                "name": upload_data["name"],
                "length": upload_data["length"],
            },
        )
