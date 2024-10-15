from abc import ABC, abstractmethod
from typing import List, Dict

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class LLMResponseStatus:
    SUCCESS: bool = True
    ERROR: bool = False



class LLMResponse(BaseModel):
    """Response from the LLM."""

    content: str = ""
    tool_calls: List[Dict] = []
    send_tokens: int = 0
    recv_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = ""
    status: int = LLMResponseStatus.ERROR


class BaseLLMConfig(BaseSettings):
    llm_type: str = ""
    api_key: str = ""
    api_base: str = ""
    chat_model: str = ""
    text_model: str = ""
    temperature: float = 0.9
    top_p: float = 1
    max_tokens: int = 4096
    timeout: int = 30
    enable_langfuse: bool = False


class BaseLLM(ABC):
    def __init__(self, config: BaseLLMConfig):
        self.config = config
        self.llm_type = config.llm_type
        self.api_key = config.api_key
        self.api_base = config.api_base
        self.chat_model = config.chat_model
        self.text_model = config.text_model
        self.temperature = config.temperature
        self.top_p = config.top_p
        self.max_tokens = config.max_tokens
        self.timeout = config.timeout
        self.enable_langfuse = config.enable_langfuse

    @abstractmethod
    def chat_completions(self, messages: List[Dict], tools: List[Dict]) -> LLMResponse:
        pass

    @abstractmethod
    def text_completions(self, prompt: str) -> LLMResponse:
        pass
