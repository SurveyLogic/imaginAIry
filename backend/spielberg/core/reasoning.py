import logging
from typing import List


from spielberg.agents.base import BaseAgent, AgentStatus, AgentResponse
from spielberg.core.session import (
    Session,
    OutputMessage,
    InputMessage,
    ContextMessage,
    RoleTypes,
    TextContent,
    MsgStatus,
)
from spielberg.llm.base import LLMResponse
from spielberg.llm.openai import OpenAI


logger = logging.getLogger(__name__)


REASONING_SYSTEM_PROMPT = """
    Act as a reasoning engine. You can reason the messages and take actions using the agents. also provide instructions for the agents.

    To respond to the user's request, follow these steps:
    1. Consider the available agents and their capabilities to complete user request to the user's message. 
    2. Provide the instructions to the agents to complete the user request.
    3. Use the agents to complete the user request.
    4. Generate the response to the user's message based on the agents' output and the user's message.
    5. Repeat the process until the user request is completed.
    6. User stop to end the conversation.
    7. If some agent requires video_id which is not available but user is asking to perform some action on some clip or generated stream.
       - 7.1. Download the stream first using download agent
       - 7.2. Upload that downloaded stream to VideoDB to get video id.
       - 7.3. Perform the initial action which required video id.
    """.strip()

SUMMARIZATION_PROMPT = """
Generate succinct summary for the user stating what all happened with agents on basis of above responses by agents.
Agent responses are already displayed to the user until specified explicitly in which case include the responses in the summary.
"""


class ReasoningEngine:
    """The Reasoning Engine is the core class that directly interfaces with the user. It interprets natural language input in any conversation and orchestrates agents to fulfill the user's requests. The primary functions of the Reasoning Engine are:

    * Maintain Context of Conversational History: Manage memory, context limits, input, and output experiences to ensure coherent and context-aware interactions.
    * Natural Language Understanding (NLU): Uses LLMs of your choice to have understanding of the task.
    * Intelligent Reference Deduction: Intelligently deduce references to previous messages, outputs, files, agents, etc., to provide relevant and accurate responses.
    * Agent Orchestration: Decide on agents and their workflows to fulfill requests. Multiple strategies can be employed to create agent workflows, such as step-by-step processes or chaining of agents provided by default.
    * Final Control Over Conversation Flow: Maintain ultimate control over the flow of conversation with the user, ensuring coherence and goal alignment."""

    def __init__(
        self,
        input_message: InputMessage,
        session: Session,
    ):
        """Initialize the ReasoningEngine.

        :param input_message: The input message to the reasoning engine.
        :param session: The session instance.
        """
        self.input_message = input_message
        self.session = session
        self.system_prompt = REASONING_SYSTEM_PROMPT
        self.max_iterations = 10
        self.llm = OpenAI()
        self.agents: List[BaseAgent] = []
        self.stop_flag = False
        self.output_message: OutputMessage = self.session.output_message

    def register_agents(self, agents: List[BaseAgent]):
        """Register an agents.

        :param agents: The list of agents to register.
        """
        self.agents.extend(agents)

    def build_context(self):
        """Build the context for the reasoning engine and Agents."""
        input_context = ContextMessage(
            content=self.input_message.content, role=RoleTypes.user
        )
        if self.session.reasoning_context:
            self.session.reasoning_context.append(input_context)
        else:
            if self.session.video_id:
                video = self.session.state["video"]
                self.session.reasoning_context.append(
                    ContextMessage(
                        content=self.system_prompt
                        + f"""\nThis is a video in the collection titled {self.session.state["collection"].name} collection_id is {self.session.state["collection"].id} \nHere is the video refer to this for search, summary and editing \n- title: {video.name}, video_id: {video.id}, media_description: {video.description}, length: {video.length}"""
                    )
                )
            else:
                videos = self.session.state["collection"].get_videos()
                video_title_list = []
                for video in videos:
                    video_title_list.append(
                        f"\n- title: {video.name}, video_id: {video.id}, media_description: {video.description}, length: {video.length}, video_stream: {video.stream_url}"
                    )
                video_titles = "\n".join(video_title_list)
                images = self.session.state["collection"].get_images()
                image_title_list = []
                for image in images:
                    image_title_list.append(
                        f"\n- title: {image.name}, image_id: {image.id}, url: {image.url}"
                    )
                image_titles = "\n".join(image_title_list)
                self.session.reasoning_context.append(
                    ContextMessage(
                        content=self.system_prompt
                        + f"""\nThis is a collection of videos and the collection description is {self.session.state["collection"].description} and collection_id is {self.session.state["collection"].id} \n\nHere are the videos in this collection user may refer to them for search, summary and editing {video_titles}\n\nHere are the images in this collection {image_titles}"""
                    )
                )
            self.session.reasoning_context.append(input_context)

    def get_current_run_context(self):
        for i in range(len(self.session.reasoning_context) - 1, -1, -1):
            if self.session.reasoning_context[i].role == RoleTypes.user:
                return self.session.reasoning_context[i:]
        return []

    def run_agent(self, agent_name: str, *args, **kwargs) -> AgentResponse:
        """Run an agent.

        :param str agent_name: The name of the agent to run
        :param args: The arguments to pass to the agent
        :param kwargs: The keyword arguments to pass to the agent
        :return: The response from the agent
        """
        print("-" * 40, f"Running {agent_name} Agent", "-" * 40)
        print(kwargs, "\n\n")

        agent = next(
            (agent for agent in self.agents if agent.agent_name == agent_name), None
        )
        self.output_message.actions.append(f"Running @{agent_name} agent")
        self.output_message.agents.append(agent_name)
        self.output_message.push_update()
        return agent.safe_call(*args, **kwargs)

    def stop(self):
        """Flag the tool to stop processing and exit the run() thread."""
        self.stop_flag = True

    def step(self):
        """Run a single step of the reasoning engine."""
        status = AgentStatus.ERROR
        temp_messages = []
        max_tries = 1
        tries = 0

        while status != AgentStatus.SUCCESS:
            if self.stop_flag:
                break

            tries += 1
            if tries > max_tries:
                break
            print("-" * 40, "Context", "-" * 40)
            print(
                [message.to_llm_msg() for message in self.session.reasoning_context],
                "\n\n",
            )
            llm_response: LLMResponse = self.llm.chat_completions(
                messages=[
                    message.to_llm_msg() for message in self.session.reasoning_context
                ]
                + temp_messages,
                tools=[agent.to_llm_format() for agent in self.agents],
            )
            logger.info(f"LLM Response: {llm_response}")

            if not llm_response.status:
                # TODO: Handle llm error
                break

            if llm_response.tool_calls:
                self.session.reasoning_context.append(
                    ContextMessage(
                        content=llm_response.content,
                        tool_calls=llm_response.tool_calls,
                        role=RoleTypes.assistant,
                    )
                )
                for tool_call in llm_response.tool_calls:
                    agent_response: AgentResponse = self.run_agent(
                        tool_call["tool"]["name"],
                        **tool_call["tool"]["arguments"],
                    )
                    self.session.reasoning_context.append(
                        ContextMessage(
                            content=agent_response.__str__(),
                            tool_call_id=tool_call["id"],
                            role=RoleTypes.tool,
                        )
                    )
                    print("-" * 40, "Agent Response", "-" * 40)
                    print(agent_response, "\n\n")
                    status = agent_response.status

            if (
                llm_response.finish_reason == "stop"
                or llm_response.finish_reason == "end_turn"
                or self.iterations == 0
            ):
                self.session.reasoning_context.append(
                    ContextMessage(
                        content=llm_response.content,
                        role=RoleTypes.assistant,
                    )
                )
                summary = TextContent()
                summary.status = MsgStatus.progress
                if self.iterations == self.max_iterations - 1:
                    # Direct response case
                    summary.status_message = "Here is the summary of the response"
                    summary.text = llm_response.content
                    summary.status = MsgStatus.success
                    self.output_message.content.append(summary)
                else:
                    summary.status_message = "Summarzing the run.."
                    self.output_message.push_update()
                    self.session.reasoning_context.append(
                        ContextMessage(
                            content=SUMMARIZATION_PROMPT.format(
                                query=self.input_message.content
                            ),
                            role=RoleTypes.system,
                        )
                    )
                    summary_response = self.llm.chat_completions(
                        messages=[
                            message.to_llm_msg()
                            for message in self.get_current_run_context()
                        ]
                    )
                    summary.text = summary_response.content
                    summary.status = MsgStatus.success
                    summary.status_message = "Here is the summary of the run"
                    self.output_message.content.append(summary)
                self.output_message.status = MsgStatus.success
                self.output_message.publish()
                print("-" * 40, "Stopping", "-" * 40)
                self.stop()
                break

    def run(self, max_iterations: int = None):
        """Run the reasoning engine.

        :param int max_iterations: The number of max_iterations to run the reasoning engine
        """
        self.iterations = max_iterations or self.max_iterations
        self.build_context()
        self.output_message.actions.append("Reasoning the message..")
        self.output_message.push_update()

        it = 0
        while self.iterations > 0:
            self.iterations -= 1
            print("-" * 40, "Reasoning Engine Iteration", it, "-" * 40)
            if self.stop_flag:
                break

            self.step()
            it = it + 1

        self.session.save_context_messages()
        print("-" * 40, "Reasoning Engine Finished", "-" * 40)
