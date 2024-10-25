import logging
import textwrap
from dataclasses import dataclass
import json

from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus
from spielberg.core.session import (
    Session,
    ContextMessage,
    RoleTypes,
    VideoContent,
    VideoData,
    MsgStatus,
)
from spielberg.tools.videodb_tool import VideoDBTool
from spielberg.llm.openai import OpenAI, OpenaiConfig


from videodb.asset import VideoAsset, TextAsset, TextStyle

logger = logging.getLogger(__name__)

SUBTITLE_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "video_id": {
            "type": "string",
            "description": "The unique identifier of the video to which subtitles will be added.",
        },
        "collection_id": {
            "type": "string",
            "description": "The unique identifier of the collection containing the video.",
        },
        "language": {
            "type": "string",
            "description": "The language the user wants the subtitles in",
        },
        "notes": {
            "type": "string",
            "description": "if user has additional requirements for the style of language",
        },
    },
    "required": ["video_id", "collection_id"],
}


translater_prompt = """

Task Description:
---
You are provided with a transcript of a video in a compact format called compact_list to optimize context size. The transcript is presented as a single string where each word block is formatted as:

word|start|end

word: The word itself.
start: The start time of the word in the video.
end: The end time of the word in the video.

Example Input (compact_list):

[ 'hello|0|10',  'world|11|12',  'how are you|13|15']

Your Task:
---
1.Translate the Text into [TARGET LANGUAGE]:
Translate all the words in the transcript from the source language to [TARGET LANGUAGE].

2.Combine Words into Meaningful Phrases or Sentences:
Group the translated words into logical phrases or sentences that make sense together.
Ensure each group is suitable for subtitle usage—neither too long nor too short.
Adjust Timing for Each Phrase/Block:

3.For each grouped phrase or sentence:
Start Time: Use the start time of the first word in the group.
End Time: Use the end time of the last word in the group.


4.Produce the Final Output:
Provide a list of subtitle blocks in the following format:
[    {"start": 0, "end": 30, "text": "Translated block of text here"},    {"start": 31, "end": 55, "text": "Another translated block of text"},    ...]
Ensure the translated text is coherent and appropriately grouped for subtitles.

Guidelines:
---

Coherence: The translated phrases should be grammatically correct and natural in [TARGET LANGUAGE].
Subtitle Length: Each subtitle block should follow standard subtitle length guidelines (e.g., no more than two lines of text, appropriate reading speed).
Timing Accuracy: Maintain accurate synchronization with the video's audio by correctly calculating start and end times.
Punctuation and Formatting: Use proper punctuation and formatting suitable for subtitles in [TARGET LANGUAGE].


Example Output:
---
If translating to Spanish, your output might look like:

you should return json of this format
{
subtitles: [    {"start": 0, "end": 30, "text": "Bloque traducido de texto aquí"},    {"start": 31, "end": 55, "text": "Otro bloque de texto traducido"},    ...]
}

Notes:
---
Be mindful of linguistic differences that may affect how words are grouped in [TARGET LANGUAGE].
Ensure that cultural nuances and idiomatic expressions are appropriately translated.

"""


class SubtitleAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "subtitle"
        self.description = "An agent designed to add different languages subtitles to a specified video within VideoDB. "
        self.llm = OpenAI(config=OpenaiConfig(timeout=120))
        self.parameters = SUBTITLE_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def wrap_text(self, text,  video_width, max_width_percent=0.60, avg_char_width=20):
        max_width_pixels = video_width * max_width_percent
        max_chars_per_line = int(max_width_pixels / avg_char_width)

        # Wrap the text based on the calculated max characters per line
        wrapped_text = "\n".join(textwrap.wrap(text, max_chars_per_line))
        return wrapped_text



    def get_compact_transcript(self, transcript):
        compact_list = []
        for word_block in transcript:
            word = word_block["text"]
            start = word_block["start"]
            end = word_block["end"]
            compact_word = f"{word}|{start}|{end}"
            if word == "-":
                continue
            compact_list.append(compact_word)
        return compact_list

    def add_subtitles_using_timeline(self, subtitles):
        video_width = 1920  
        timeline = self.videodb_tool.get_and_set_timeline()
        video_asset = VideoAsset(asset_id=self.video_id)
        timeline.add_inline(video_asset)
        previous_end = None
        for subtitle_chunk in subtitles:
            start = round(subtitle_chunk["start"], 2)
            end = round(subtitle_chunk["end"], 2)
            diff = round(end - start, 2)
            
            if previous_end is not None and start <= previous_end:
                start = previous_end + 0.01  # Ensure no overlap
            
            wrapped_text = self.wrap_text(subtitle_chunk["text"], video_width)
            style = TextStyle(
                fontsize=20,
                fontcolor="white",
                box=True,
                boxcolor="black@0.6",
                boxborderw="5",
                y="main_h-text_h-75"
            )
            text_asset = TextAsset(
                text=wrapped_text,
                duration=diff,
                style=style,
            )
            print(f"Adding subtitle from {start} to {end}, {wrapped_text}, {text_asset}")
            timeline.add_overlay(start=start, asset=text_asset)
            previous_end = end
        stream_url = timeline.generate_stream()
        return stream_url

    def run(
        self,
        video_id: str,
        collection_id: str,
        language: str = "english",
        notes: str = "",
        *args,
        **kwargs,
    ) -> AgentResponse:
        """
        Adds subtitles to the specified video using the provided style configuration.

        :param str video_id: The unique identifier of the video to process.
        :param str collection_id: The unique identifier of the collection containing the video.
        :param str language: A string specifying the language for the subtitles.
        :param str notes: A String specifying the style of the language used in subtitles
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response indicating the success or failure of the subtitle addition operation.
        :rtype: AgentResponse
        """
        try:
            self.collection_id = collection_id
            self.video_id = video_id
            if collection_id is None:
                self.videodb_tool = VideoDBTool()
            else:
                self.videodb_tool = VideoDBTool(collection_id=collection_id)

            self.output_message.actions.append(
                "Retrieving the subtitles in the video's original language"
            )
            self.output_message.push_update()

            video_content = VideoContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Processing...",
            )
            self.output_message.content.append(video_content)
            self.output_message.push_update()

            transcript = self.videodb_tool.get_transcript(video_id, text=False)
            compact_transcript = self.get_compact_transcript(transcript=transcript)

            self.output_message.actions.append(
                f"Translating the subtitles to {language}"
            )
            self.output_message.push_update()
            profanity_prompt = f"{translater_prompt} Translate to {language}, additional notes : {notes} compact_list: {compact_transcript}"
            profanity_llm_message = ContextMessage(
                content=profanity_prompt,
                role=RoleTypes.user,
            )
            llm_response = self.llm.chat_completions(
                [profanity_llm_message.to_llm_msg()],
                response_format={"type": "json_object"},
            )
            translated_subtitles = json.loads(llm_response.content)

            if notes:
                self.output_message.actions.append(
                    f"Refining the language with additional notes: {notes}"
                )
                self.output_message.push_update()

            self.output_message.actions.append(
                "Overlaying the translated subtitles onto the video"
            )
            self.output_message.push_update()

            stream_url = self.add_subtitles_using_timeline(
                translated_subtitles["subtitles"]
            )
            video_content.video = VideoData(stream_url=stream_url)
            video_content.status = MsgStatus.success
            video_content.status_message = f"Subtitles in {language} have been successfully added to your video. Here is your stream."
            self.output_message.publish()

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent: {e}")
            video_content.status = MsgStatus.error
            video_content.status_message = (
                "An error occurred while adding subtitles to the video."
            )
            self.output_message.content.append(video_content)
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="Subtitles added successfully",
            data={stream_url: stream_url},
        )
