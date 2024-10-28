import logging
import json
import concurrent.futures

from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import (
    Session,
    ContextMessage,
    RoleTypes,
    MsgStatus,
    VideoContent,
    VideoData,
)
from director.tools.videodb_tool import VideoDBTool
from director.llm.openai import OpenAI

logger = logging.getLogger(__name__)

PROMPTCLIP_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "prompt": {
            "type": "string",
            "description": "Prompt to generate clip",
        },
        "video_id": {
            "type": "string",
            "description": "Video Id to generate clip",
        },
        "collection_id": {
            "type": "string",
            "description": "Collection Id to of the video",
        },
    },
    "required": ["prompt", "video_id", "collection_id"],
}


class PromptClipAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "prompt_clip"
        self.description = "Generates video clips based on user prompts. This agent uses AI to analyze the text of a video transcript and identify sentences relevant to the user prompt for making clips. It then generates video clips based on the identified sentences. Use this tool to create clips based on specific themes or topics from a video."
        self.parameters = PROMPTCLIP_AGENT_PARAMETERS
        self.llm = OpenAI()
        super().__init__(session=session, **kwargs)

    def _chunk_docs(self, docs, chunk_size):
        """
        chunk docs to fit into context of your LLM
        :param docs:
        :param chunk_size:
        :return:
        """
        for i in range(0, len(docs), chunk_size):
            yield docs[i : i + chunk_size]  # Yield the current chunk

    def _text_prompter(self, transcript_text, prompt):
        chunk_size = 10000
        # sentence tokenizer
        chunks = self._chunk_docs(transcript_text, chunk_size=chunk_size)

        matches = []
        prompts = []
        i = 0
        for chunk in chunks:
            chunk_prompt = """
            You are a video editor who uses AI. Given a user prompt and transcript of a video analyze the text to identify sentences in the transcript relevant to the user prompt for making clips. 
            - **Instructions**: 
            - Evaluate the sentences for relevance to the specified user prompt.
            - Make sure that sentences start and end properly and meaningfully complete the discussion or topic. Choose the one with the greatest relevance and longest.
            - We'll use the sentences to make video clips in future, so optimize for great viewing experience for people watching the clip of these.
            - Strictly make each result minimum 20 words long. If the match is smaller, adjust the boundries and add more context around the sentences.

            - **Output Format**: Return a JSON list of strings named 'sentences' that containes the output sentences, make sure they are exact substrings.
            - **User Prompts**: User prompts may include requests like 'find funny moments' or 'find moments for social media'. Interpret these prompts by 
            identifying keywords or themes in the transcript that match the intent of the prompt.
            """
            # pass the data
            chunk_prompt += f"""
            Transcript: {chunk}
            User Prompt: {prompt}
            """
            # Add instructions to always return JSON at the end of processing.
            chunk_prompt += """
            Ensure the final output strictly adheres to the JSON format specified without including additional text or explanations. \
            If there is no match return empty list without additional text. Use the following structure for your response:
            {
            "sentences": [
                {},
                ...
            ]
            }
            """
            prompts.append(chunk_prompt)
            i += 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_index = {
                executor.submit(
                    self.llm.chat_completions,
                    [
                        ContextMessage(
                            content=prompt, role=RoleTypes.user
                        ).to_llm_msg()
                    ],
                    response_format={"type": "json_object"},
                ): i
                for i, prompt in enumerate(prompts)
            }
            for future in concurrent.futures.as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    llm_response = future.result()
                    if not llm_response.status:
                        logger.error(f"LLM failed with {llm_response.content}")
                        continue
                    output = json.loads(llm_response.content)
                    matches.extend(output["sentences"])
                except Exception as e:
                    logger.exception(f"Error in getting matches: {e}")
                    continue
        return matches

    def run(
        self, prompt: str, video_id: str, collection_id: str, *args, **kwargs
    ) -> AgentResponse:
        try:
            videodb_tool = VideoDBTool(collection_id=collection_id)
            self.output_message.actions.append("Retrieving video transcript..")
            self.output_message.push_update()
            try:
                transcript_text = videodb_tool.get_transcript(video_id)
            except Exception:
                self.output_message.actions.append(
                    "Transcript unavailable. Indexing spoken content."
                )
                self.output_message.push_update()
                videodb_tool.index_spoken_words(video_id)
                transcript_text = videodb_tool.get_transcript(video_id)

            self.output_message.actions.append("Identifying key moments..")
            self.output_message.push_update()
            result = self._text_prompter(transcript_text, prompt)
            result_timestamps = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_index = {
                    executor.submit(
                        videodb_tool.keyword_search, description, video_id
                    ): description
                    for description in result
                }
                for future in concurrent.futures.as_completed(future_to_index):
                    description = future_to_index[future]
                    try:
                        search_res = future.result()
                        matched_segments = search_res.get_shots()
                        video_shot = matched_segments[0]
                        result_timestamps.append(
                            (video_shot.start, video_shot.end, video_shot.text)
                        )
                    except Exception as e:
                        logger.error(
                            f"Error in getting timestamps of {description}: {e}"
                        )
                        continue
            if result_timestamps:
                try:
                    self.output_message.actions.append("Key moments identified..")
                    self.output_message.actions.append("Creating video clip..")
                    video_content = VideoContent(
                        agent_name=self.agent_name, status=MsgStatus.progress
                    )
                    self.output_message.content.append(video_content)
                    self.output_message.push_update()
                    timeline = []
                    for timestamp in result_timestamps:
                        timeline.append((timestamp[0], timestamp[1]))
                    stream_url = videodb_tool.generate_video_stream(
                        video_id=video_id, timeline=timeline
                    )
                    video_content.status_message = "Clip generated successfully."
                    video_content.video = VideoData(stream_url=stream_url)
                    video_content.status = MsgStatus.success
                    self.output_message.publish()

                except Exception as e:
                    logger.exception(f"Error in creating video content: {e}")
                    return AgentResponse(status=AgentStatus.ERROR, message=str(e))

                return AgentResponse(
                    status=AgentStatus.SUCCESS,
                    message=f"Agent {self.name} completed successfully.",
                    data={"stream_url": stream_url},
                )
            else:
                return AgentResponse(
                    status=AgentStatus.ERROR,
                    message="No relevant moments found.",
                )

        except Exception as e:
            logger.exception(f"error in {self.agent_name}")
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))
