import logging

from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, MsgStatus, TextContent

logger = logging.getLogger(__name__)


class SampleAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "sample"
        self.description = "Sample agent description"
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def run(self, sample_id: str, *args, **kwargs) -> AgentResponse:
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
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Generating sample response..",
            )
            self.output_message.content.append(text_content)
            self.output_message.push_update()
            text_content.text = "This is the text result of Agent."
            text_content.status = MsgStatus.success
            text_content.status_message = "Here is your response"
            self.output_message.publish()
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content.status = MsgStatus.error
            text_content.status_message = "Error in calculating pricing."
            self.output_message.publish()
            error_message = f"Agent failed with error {e}"
            return AgentResponse(status=AgentStatus.ERROR, message=error_message)
        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message=f"Agent {self.name} completed successfully.",
            data={},
        )
