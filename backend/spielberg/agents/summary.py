import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult
from spielberg.core.session import ContextMessage, RoleTypes, TextContent, MsgStatus
from spielberg.llm.openai import OpenaiConfig, OpenAI
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

SUMMARY_AGENT_PROMPT = """
Generate a summary of following transcript:
"""


class SummaryAgent(BaseAgent):
    def __init__(self, session=None, **kwargs):
        self.agent_name = "summary"
        self.description = "This is an agent to summarize the given video of VideoDB."
        self.llm = OpenAI(OpenaiConfig())
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def __call__(self, collection_id: str, video_id: str) -> AgentResponse:
        """
        Generate summary of the given video.
        """
        try:
            self.output_message.actions.append("Generating summary.")
            text_content = TextContent(agent_name=self.agent_name)
            self.output_message.content.append(text_content)
            self.output_message.push_update()

            videodb_tool = VideoDBTool()
            try:
                transcript_text = videodb_tool.get_transcript(collection_id, video_id)
            except Exception:
                logger.error("Failed to get transcript, indexing")
                transcript_text = videodb_tool.index_spoken_words(
                    collection_id, video_id
                )
                transcript_text = videodb_tool.get_transcript(collection_id, video_id)
            summary_llm_message = f"{SUMMARY_AGENT_PROMPT} {transcript_text}"
            summary_llm_context = ContextMessage(
                content=summary_llm_message, role=RoleTypes.user
            )
            llm_response = self.llm.chat_completions([summary_llm_context.to_llm_msg()])
            if not llm_response.status:
                logger.error(f"LLM failed with {llm_response}")
                return AgentResponse(
                    result=AgentResult.ERROR,
                    message="Summary failed due to LLM error.",
                )

            text_content.text = llm_response.content
            text_content.status = MsgStatus.success
            text_content.status_message = "Summary generated successfully."
            self.output_message.publish()

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent.")
            text_content.status = MsgStatus.error
            text_content.status_message = "Error in generating summary."
            self.output_message.publish()
            return AgentResponse(result=AgentResult.ERROR, message=str(e))

        return AgentResponse(
            result=AgentResult.SUCCESS,
            message="Summary generated.",
            data={"message": "Summary generated."},
        )
