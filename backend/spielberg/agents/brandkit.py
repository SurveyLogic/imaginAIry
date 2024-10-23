import os
import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus
from spielberg.core.session import Session, MsgStatus, VideoContent
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

INTRO_VIDEO_ID = os.getenv("INTRO_VIDEO_ID")
OUTRO_VIDEO_ID = os.getenv("OUTRO_VIDEO_ID")
BRAND_IMAGE_ID = os.getenv("BRAND_IMAGE_ID")


class BrandkitAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "brandkit"
        self.description = (
            "Agent to add brand kit elements (intro video, outro video and brand image) to the given video in VideoDB,"
            "if user has not given those optional param of intro video, outro video and brand image always try with sending them as None so that defaults are picked from env"
        )
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def run(
        self,
        collection_id: str,
        video_id: str,
        intro_video_id: str = None,
        outro_video_id: str = None,
        brand_image_id: str = None,
        *args,
        **kwargs,
    ) -> AgentResponse:
        """
        Generate stream of video after adding branding elements.

        :param str collection_id: collection id in which videos are available.
        :param str video_id: video id on which branding is required.
        :param str intro_video_id: VideoDB video id of intro video, defaults to INTRO_VIDEO_ID
        :param str outro_video_id: video id of outro video, defaults to OUTRO_VIDEO_ID
        :param str brand_image_id: image id of brand image for overlay over video, defaults to BRAND_IMAGE_ID
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the generated brand stream.
        :rtype: AgentResponse
        """
        try:
            self.output_message.actions.append("Processing brandkit request..")
            intro_video_id = intro_video_id or INTRO_VIDEO_ID
            outro_video_id = outro_video_id or OUTRO_VIDEO_ID
            brand_image_id = brand_image_id or BRAND_IMAGE_ID
            if not any([intro_video_id, outro_video_id, brand_image_id]):
                message = (
                    "Branding elementes not provided, either you can provide provide IDs for intro video, outro video and branding image"
                    " or you can set INTRO_VIDEO_ID, OUTRO_VIDEO_ID and BRAND_IMAGE_ID in .env of backend directory."
                )
                return AgentResponse(status=AgentStatus.ERROR, message=message)
            video_content = VideoContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Generating video with branding..",
            )
            self.output_message.content.append(video_content)
            self.output_message.push_update()
            videodb_tool = VideoDBTool(collection_id=collection_id)
            brandkit_stream = videodb_tool.add_brandkit(
                video_id, intro_video_id, outro_video_id, brand_image_id
            )
            video_content.video = {"stream_url": brandkit_stream}
            video_content.status = MsgStatus.success
            video_content.status_message = "Here is your brandkit stream"
            self.output_message.publish()
        except Exception:
            logger.exception(f"Error in {self.agent_name}")
            video_content.status = MsgStatus.error
            error_message = "Error in adding branding."
            video_content.status_message = error_message
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=error_message)
        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message=f"Agent {self.name} completed successfully.",
            data={"stream_url": brandkit_stream},
        )
