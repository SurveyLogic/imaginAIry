import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult

from spielberg.core.session import Session, MsgStatus, ImageContent
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
            "description": "Timestamp in seconds of the video to generate thumbnail",
        },
    },
    "required": ["collection_id", "video_id"],
}


class ThumbnailAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "thumbnail"
        self.description = "Generates a thumbnail image from a video file at a specified timestamp. This Agent takes a video id and a timestamp as input, and produces a representative image frame at that precise moment in the video. It extracts the exact frame from the video at the given time. Use this tool when a user requests a preview, snapshot, generate or visual representation of a specific moment in a video file. The output is a static image file suitable for quick previews or thumbnails. It will not provide any other processing or editing options beyond generating the thumbnail."
        self.parameters = THUMBNAIL_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def __call__(
        self, collection_id: str, video_id: str, timestamp: int = 5, *args, **kwargs
    ) -> AgentResponse:
        """
        Get the thumbnail for the video at the given timestamp
        """
        try:
            self.output_message.actions.append("Generating thumbnail.")
            image_content = ImageContent(agent_name=self.agent_name)
            self.output_message.content.append(image_content)
            self.output_message.push_update()

            videodb_tool = VideoDBTool(collection_id=collection_id)
            thumbnail_data = videodb_tool.generate_thumbnail(
                video_id=video_id, timestamp=timestamp
            )

            image_content.image = thumbnail_data
            image_content.status = MsgStatus.success
            image_content.status_message = "Thumbnail generated successfully."
            self.output_message.publish()

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent.")
            image_content.status = MsgStatus.error
            image_content.status_message = "Error in generating thumbnail."
            self.output_message.publish()
            return AgentResponse(result=AgentResult.ERROR, message=str(e))

        return AgentResponse(
            result=AgentResult.SUCCESS,
            message="Thumbnail fetched",
            data=thumbnail_data,
        )
