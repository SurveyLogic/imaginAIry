import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus

from spielberg.core.session import Session, MsgStatus, ImageContent, ImageData
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

THUMBNAIL_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "collection_id": {
            "type": "string",
            "description": "Collection Id to of the video",
        },
        "video_id": {
            "type": "string",
            "description": "Video Id to generate thumbnail",
        },
        "timestamp": {
            "type": "integer",
            "description": "Timestamp in seconds of the video to generate thumbnail, Optional parameter don't ask from user",
        },
    },
    "required": ["collection_id", "video_id"],
}


class ThumbnailAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "thumbnail"
        self.description = "Generates a thumbnail image from a video file. This Agent takes a video id and a optionl timestamp as input. Use this tool when a user requests a preview, snapshot, generate or visual representation of a specific moment in a video file. The output is a static image file suitable for quick previews or thumbnails. It will not provide any other processing or editing options beyond generating the thumbnail."
        self.parameters = THUMBNAIL_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def run(
        self, collection_id: str, video_id: str, timestamp: int = 5, *args, **kwargs
    ) -> AgentResponse:
        """
        Get the thumbnail for the video at the given timestamp
        """
        try:
            self.output_message.actions.append("Generating thumbnail..")
            image_content = ImageContent(agent_name=self.agent_name)
            self.output_message.content.append(image_content)
            self.output_message.push_update()

            videodb_tool = VideoDBTool(collection_id=collection_id)
            thumbnail_data = videodb_tool.generate_thumbnail(
                video_id=video_id, timestamp=timestamp
            )
            image_content.image = ImageData(**thumbnail_data)
            image_content.status = MsgStatus.success
            image_content.status_message = "Here is your thumbnail."
            self.output_message.publish()

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent.")
            image_content.status = MsgStatus.error
            image_content.status_message = "Error in generating thumbnail."
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="Thumbnail generated and displayed to user.",
            data=thumbnail_data,
        )
