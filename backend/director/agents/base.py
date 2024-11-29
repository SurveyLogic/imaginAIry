import logging

from abc import ABC, abstractmethod
from pydantic import BaseModel

from openai_function_calling import FunctionInferrer

from director.core.session import Session, OutputMessage, TextContent, MsgStatus

logger = logging.getLogger(__name__)


class AgentStatus:
    SUCCESS = "success"
    ERROR = "error"


class AgentResponse(BaseModel):
    """Data model for respones from agents."""

    status: str = AgentStatus.SUCCESS
    message: str = ""
    data: dict = {}


class BaseAgent(ABC):
    """Interface for all agents. All agents should inherit from this class."""

    def __init__(self, session: Session, **kwargs):
        self.session: Session = session
        self.output_message: OutputMessage = self.session.output_message

    def get_parameters(self):
        """Return the automatically inferred parameters for the function using the dcstring of the function."""
        function_inferrer = FunctionInferrer.infer_from_function_reference(self.run)
        function_json = function_inferrer.to_json_schema()
        parameters = function_json.get("parameters")
        if not parameters:
            raise Exception(
                "Failed to infere parameters, please define JSON instead of using this automated util."
            )
        return parameters

    def _check_supported_llm(self):
        """Check if supported_llm is present and validate LLM."""
        if hasattr(self, "supported_llm") and hasattr(self, "llm"):
            if self.llm.llm_type not in self.supported_llm:
                error = f"`@{self.agent_name}` Agent does not support the configured LLM `{self.llm.llm_type.upper()}`, To use this Agent, please configure one of the following LLMs: {[llm.upper() for llm in self.supported_llm]}."
                self.output_message.content.append(
                    TextContent(
                        status_message="LLM not supported.",
                        text=error,
                        status=MsgStatus.error,
                    )
                )
                raise Exception(error)

    def to_llm_format(self):
        """Convert the agent to LLM tool format."""
        return {
            "name": self.agent_name,
            "description": self.description,
            "parameters": self.parameters,
        }

    @property
    def name(self):
        return self.agent_name

    @property
    def agent_description(self):
        return self.description

    def safe_call(self, *args, **kwargs):
        try:
            self._check_supported_llm()
            return self.run(*args, **kwargs)

        except Exception as e:
            logger.exception(f"error in {self.agent_name} agent: {e}")
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

    @abstractmethod
    def run(*args, **kwargs) -> AgentResponse:
        pass
