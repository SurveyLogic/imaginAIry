import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult
from spielberg.core.session import Session, MsgStatus, VideoContent
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)


class StreamVideoAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "stream_video"
        self.description = (
            "Agent to get the video player of the existing video or given m3u8 stream_url"
        )
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def __call__(
        self,
        collection_id: str = None,
        video_id: str = None,
        stream_url: str = None,
        *args,
        **kwargs,
    ) -> AgentResponse:
        """
        Process the collection_id, video_id or stream_url to send the video component.

        :param str collection_id: The collection_id where given video_id is available.
        :param str video_id: The id of the video for which the video player is required.
        :param str stream_url: stream_url for which video player is required.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the sample processing operation.
        :rtype: AgentResponse
        """
        try:
            if video_id:
                self.output_message.actions.append("Processing for given video_id..")
            elif stream_url:
                self.output_message.actions.append("Processing given stream url..")
            else:
                return AgentResponse(
                    result=AgentResult.ERROR,
                    message="Either 'video_id' or 'stream_url' is required for getting the stream in video player.",
                )
            if stream_url:
                video_content = VideoContent(
                    agent_name=self.agent_name,
                    status=MsgStatus.success,
                    status_message="Here is your stream",
                    video={"stream_url": stream_url},
                )
                self.output_message.content.append(video_content)
                self.output_message.publish()
                return AgentResponse(
                    result=AgentResult.SUCCESS,
                    message=f"Agent {self.name} completed successfully.",
                    data={},
                )
            video_content = VideoContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Loading stream for the video..",
            )
            self.output_message.content.append(video_content)
            self.output_message.push_update()
            videodb_tool = VideoDBTool(collection_id=collection_id)
            video_data = videodb_tool.get_video(video_id)
            stream_url = video_data.get("stream_url")
            video_content.video = {
                "stream_url": stream_url,
            }
            video_content.status = MsgStatus.success
            video_content.status_message = "Here is your stream"
            self.output_message.publish()
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            video_content.status = MsgStatus.error
            video_content.status_message = "Error in calculating pricing."
            self.output_message.publish()
            error_message = f"Agent failed with error {e}"
            return AgentResponse(result=AgentResult.ERROR, message=error_message)
        return AgentResponse(
            result=AgentResult.SUCCESS,
            message=f"Agent {self.name} completed successfully.",
            data={},
        )
