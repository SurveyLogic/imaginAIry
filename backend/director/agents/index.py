import logging

from director.agents.base import BaseAgent, AgentResponse, AgentStatus

from director.core.session import Session
from director.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

INDEX_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "video_id": {
            "type": "string",
            "description": "The ID of the video to process.",
        },
        "index_type": {
            "type": "string",
            "enum": ["spoken_words", "scene"],
        },
        "collection_id": {
            "type": "string",
            "description": "The ID of the collection to process.",
        },
    },
    "required": ["video_id", "index_type", "collection_id"],
}


class IndexAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "index"
        self.description = "This is an agent to index the given video of VideoDB. The indexing can be done for spoken words or scene."
        self.parameters = INDEX_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def run(
        self, video_id: str, index_type: str, collection_id=None, *args, **kwargs
    ) -> AgentResponse:
        """
        Process the sample based on the given sample ID.
        :param str video_id: The ID of the video to process.
        :param str index_type: The type of indexing to perform.
        :param str collection_id: The ID of the collection to process.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the sample processing operation.
        :rtype: AgentResponse
        """
        try:
            scene_data = {}
            if collection_id is None:
                self.videodb_tool = VideoDBTool()
            else:
                self.videodb_tool = VideoDBTool(collection_id=collection_id)
            self.output_message.actions.append(f"Indexing {index_type} for video")
            self.output_message.push_update()

            if index_type == "spoken_words":
                self.videodb_tool.index_spoken_words(video_id)

            elif index_type == "scene":
                index_id = self.videodb_tool.index_scene(video_id)
                scene_data = {"scene_index_id": index_id}

        except Exception as e:
            logger.exception(f"error in {self.agent_name} agent: {e}")
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message=f"{index_type} indexing successful",
            data=scene_data,
        )
