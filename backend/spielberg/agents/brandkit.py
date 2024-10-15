import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentResult
from spielberg.core.session import Session, MsgStatus, TextContent

logger = logging.getLogger(__name__)


class SampleAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "brandkit"
        self.description = "Agent to add brand kit "
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def __call__(self, video_id: str, *args, **kwargs) -> AgentResponse:
        """
        Process the sample based on the given sample ID.

        :param str sample_id: The ID of the sample to process.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the sample processing operation.
        :rtype: AgentResponse
        """
        try:
            self.output_message.actions.append("Processing sample..")
            text_content = TextContent(
                agent_name=self.agent_name, status=MsgStatus.progress
            )
            self.output_message.content.append(text_content)
            self.output_message.push_update()
            text_content.text = "This is the text result of Agent."
            text_content.status = MsgStatus.success
            self.output_message.publish()
        except Exception:
            logger.exception(f"error in {self.agent_name}")
            text_content.status = MsgStatus.error
            error_message = "Error in calculating pricing."
            text_content.status_message = error_message
            self.output_message.publish()
            return AgentResponse(result=AgentResult.ERROR, message=error_message)
        return AgentResponse(
            result=AgentResult.SUCCESS,
            message=f"Agent {self.name} completed successfully.",
            data={},
        )
