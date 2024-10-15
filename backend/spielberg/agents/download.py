import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult
from spielberg.core.session import Session
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)


class DownloadAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "download"
        self.description = "Get the download URLs of the VideoDB generated streams."
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def __call__(
        self, stream_link: str, name: str = None, *args, **kwargs
    ) -> AgentResponse:
        """
        Downloads the video from the given stream link.

        :param stream_link: The URL of the video stream to download.
        :type stream_link: str
        :param stream_name: Optional name for the video stream. If not provided, defaults to None.
        :type stream_name: str, optional
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the download operation.
        :rtype: AgentResponse
        """
        try:
            videodb_tool = VideoDBTool()
            download_response = videodb_tool.download(stream_link, name)
        except Exception as e:
            logger.exception(f"error in {self.agent_name} agent: {e}")
            return AgentResponse(result=AgentResult.ERROR, message=str(e))
        return AgentResponse(
            result=AgentResult.SUCCESS,
            message="Download successful",
            data=download_response,
        )
