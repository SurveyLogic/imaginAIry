import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus
from spielberg.core.session import Session, MsgStatus, TextContent, ContextMessage, RoleTypes

logger = logging.getLogger(__name__)

# Slack App Setup:
# 1. Go to https://api.slack.com/apps and create a new app
# 2. Add the 'chat:write' OAuth scope under 'Bot Token Scopes'
# 3. Install the APP in your slack workspace
# 4. Copy the 'Bot User OAuth Token' and set it as an environment variable SLACK_BOT_TOKEN
# 5. Invite the bot to the channel where you want to send messages


class SlackAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "slack"
        self.description = "messages to a Slack channel"
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)
        self.slack_token = os.environ.get("SLACK_BOT_TOKEN")
        self.slack_client = WebClient(token=self.slack_token)

    def run(self, message: str, *args, **kwargs) -> AgentResponse:
        """
        Send a message to a Slack channel.
        :param str message: The message to send to the Slack channel_name.
        :param str channel_name: The name or ID of the Slack channel_name to send the message to. This is optional and if not provided ask the user to provide the channel_name.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing information about the Slack message operation.
        :rtype: AgentResponse
        """
        slack_llm_prompt = f"Format the following message as markdown that slack can render nicely: {message}"
        slack_message = ContextMessage(
                content=slack_llm_prompt, role=RoleTypes.user
            )
        llm_response = self.llm.chat_completions([slack_message.to_llm_msg()])
        message_formatted = llm_response.content
        
        CHANNEL_NAME = os.getenv("SLACK_CHANNEL_NAME")
        channel_name = CHANNEL_NAME
        try:
            self.output_message.actions.append("Sending message to Slack...")
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Sending message to Slack...",
            )
            self.output_message.content.append(text_content)
            self.output_message.push_update()

            # Send message to Slack
            response = self.slack_client.chat_postMessage(
                channel=channel_name,
                text=message_formatted
            )

            text_content.text = f"Message sent to Slack channel: {channel_name}"
            text_content.status = MsgStatus.success
            text_content.status_message = "Message sent successfully"
            self.output_message.publish()

            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message=f"Message sent to Slack channel: {channel_name}",
                data={"channel_name": channel_name, "ts": response["ts"]}
            )

        except SlackApiError as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content.status = MsgStatus.error
            text_content.status_message = f"Error sending message to Slack: {str(e)}"
            self.output_message.publish()
            error_message = f"Slack API error: {str(e)}"
            return AgentResponse(status=AgentStatus.ERROR, message=error_message)

        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content.status = MsgStatus.error
            text_content.status_message = f"Error in Slack agent: {str(e)}"
            self.output_message.publish()
            error_message = f"Agent failed with error: {str(e)}"
            return AgentResponse(status=AgentStatus.ERROR, message=error_message)
