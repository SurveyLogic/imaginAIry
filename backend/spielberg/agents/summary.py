import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult
from spielberg.core.session import ContextMessage, RoleTypes, TextContent, MsgStatus
from spielberg.llm.openai import OpenAI
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

SUMMARY_AGENT_PROMPT = """
Create a comprehensive, in-depth summary that is clear and concise.
Focus strictly on the main ideas and essential information from the provided text, eliminating any unnecessary language or details.
"""


class SummaryAgent(BaseAgent):
    def __init__(self, session=None, **kwargs):
        self.agent_name = "summary"
        self.description = "This is an agent to summarize the given video of VideoDB."
        self.llm = OpenAI()
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def __call__(self, collection_id: str, video_id: str) -> AgentResponse:
        """
        Generate summary of the given video.
        """
        try:
            self.output_message.actions.append("Started summary generation..")
            output_text_content = TextContent(
                agent_name=self.agent_name, status_message="Generating the summary.."
            )
            self.output_message.content.append(output_text_content)
            self.output_message.push_update()
            videodb_tool = VideoDBTool(collection_id=collection_id)
            try:
                transcript_text = videodb_tool.get_transcript(video_id)
            except Exception:
                logger.error("Failed to get transcript, indexing")
                self.output_message.actions.append("Indexing the video..")
                self.output_message.push_update()
                videodb_tool.index_spoken_words(video_id)
                transcript_text = videodb_tool.get_transcript(video_id)
            summary_llm_prompt = f"{SUMMARY_AGENT_PROMPT} {transcript_text}"
            summary_llm_message = ContextMessage(
                content=summary_llm_prompt, role=RoleTypes.user
            )
            llm_response = self.llm.chat_completions([summary_llm_message.to_llm_msg()])
            if not llm_response.status:
                logger.error(f"LLM failed with {llm_response}")
                output_text_content.status = MsgStatus.failed
                output_text_content.status_message = "Failed to generat the summary."
                self.output_message.publish()
                return AgentResponse(
                    result=AgentResult.ERROR,
                    message="Summary failed due to LLM error.",
                )
            summary = llm_response.content
            output_text_content.text = summary
            output_text_content.status = MsgStatus.success
            output_text_content.status_message = "Summary generated successfully."
            self.output_message.publish()
        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent.")
            output_text_content.status = MsgStatus.error
            output_text_content.status_message = "Error in generating summary."
            self.output_message.publish()
            return AgentResponse(result=AgentResult.ERROR, message=str(e))

        return AgentResponse(
            result=AgentResult.SUCCESS,
            message="Summary generated and displayed to user.",
            data={"summary": summary},
        )
