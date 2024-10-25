import logging
from dataclasses import dataclass

from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus
from spielberg.core.session import Session
from spielberg.tools.videodb_tool import VideoDBTool
from videodb import SubtitleStyle, SubtitleAlignment, SubtitleBorderStyle

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
        "subtitle_style": {
            "type": "object",
            "description": "A configuration object defining the visual style of the subtitles. This includes typography, color, positioning, and other stylistic options to align with your branding and guidelines.",
            "properties": {
                "font_name": {
                    "type": "string",
                    "default": "Arial",
                    "description": "The name of the font to use for the subtitle text. Example: 'Helvetica', 'Times New Roman'.",
                },
                "font_size": {
                    "type": "number",
                    "default": 18,
                    "description": "The size of the subtitle text in points. Larger values increase text size.",
                },
                "primary_colour": {
                    "type": "string",
                    "default": "&H00FFFFFF",
                    "description": "The color of the main subtitle text in '&HBBGGRR' or '&HAABBGGRR' hexadecimal format. Example: '&H00FF0000' for blue.",
                },
                "secondary_colour": {
                    "type": "string",
                    "default": "&H000000FF",
                    "description": "The color used for secondary effects like karaoke in '&HBBGGRR' or '&HAABBGGRR' format.",
                },
                "outline_colour": {
                    "type": "string",
                    "default": "&H00000000",
                    "description": "The color of the text outline in '&HBBGGRR' or '&HAABBGGRR' format.",
                },
                "back_colour": {
                    "type": "string",
                    "default": "&H00000000",
                    "description": "The background color of the subtitle box in '&HBBGGRR' or '&HAABBGGRR' format.",
                },
                "bold": {
                    "type": "boolean",
                    "default": False,
                    "description": "Set to true to make the subtitle text bold.",
                },
                "italic": {
                    "type": "boolean",
                    "default": False,
                    "description": "Set to true to italicize the subtitle text.",
                },
                "underline": {
                    "type": "boolean",
                    "default": False,
                    "description": "Set to true to underline the subtitle text.",
                },
                "strike_out": {
                    "type": "boolean",
                    "default": False,
                    "description": "Set to true to apply a strikethrough to the subtitle text.",
                },
                "scale_x": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Horizontal scaling factor for the text. A value of 1.0 means no scaling. Values greater than 1.0 stretch the text horizontally.",
                },
                "scale_y": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Vertical scaling factor for the text. A value of 1.0 means no scaling. Values greater than 1.0 stretch the text vertically.",
                },
                "spacing": {
                    "type": "number",
                    "default": 0,
                    "description": "Additional space between characters in pixels. Positive values increase spacing.",
                },
                "angle": {
                    "type": "number",
                    "default": 0,
                    "description": "Rotation angle of the subtitle text in degrees. Positive values rotate the text clockwise.",
                },
                "border_style": {
                    "type": "integer",
                    "default": 4,
                    "enum": [1, 3, 4],
                    "description": "Style of the border around the text. Options are: 1 (no border), 3 (opaque box), 4 (outline).",
                },
                "outline": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Width of the outline around the text in pixels. Higher values result in a thicker outline.",
                },
                "shadow": {
                    "type": "number",
                    "default": 0.0,
                    "description": "Depth of the shadow behind the text in pixels. Higher values create a more pronounced shadow effect.",
                },
                "alignment": {
                    "type": "integer",
                    "default": 2,
                    "enum": [1, 2, 3, 5, 6, 7, 9, 10, 11],
                    "description": (
                        "Defines the position of the subtitle text on the screen based on the numeric keypad layout:\n"
                        "1 (Bottom Left), 2 (Bottom Center), 3 (Bottom Right),\n"
                        "5 (Top Left), 6 (Top Center), 7 (Top Right),\n"
                        "9 (Middle Left), 10 (Middle Center), 11 (Middle Right)."
                    ),
                },
                "margin_l": {
                    "type": "integer",
                    "default": 10,
                    "description": "Left margin in pixels. Increases space between the left edge of the screen and the subtitle text.",
                },
                "margin_r": {
                    "type": "integer",
                    "default": 10,
                    "description": "Right margin in pixels. Increases space between the right edge of the screen and the subtitle text.",
                },
                "margin_v": {
                    "type": "integer",
                    "default": 10,
                    "description": "Vertical margin in pixels. Adjusts the space from the top or bottom edge, depending on alignment.",
                },
            },
        },
    },
    "required": ["video_id", "collection_id"],
}


class SubtitleAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "subtitle"
        self.description = (
            "An agent designed to add styled subtitles to a specified video within VideoDB. "
            "It allows extensive customization of subtitle appearance, including typography, color schemes, "
            "positioning, and text effects, to align with specific branding and style guidelines."
        )
        self.parameters = SUBTITLE_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def run(
        self,
        video_id: str,
        collection_id: str,
        subtitle_style: dict = None,
        *args,
        **kwargs,
    ) -> AgentResponse:
        """
        Adds subtitles to the specified video using the provided style configuration.

        :param str video_id: The unique identifier of the video to process.
        :param str collection_id: The unique identifier of the collection containing the video.
        :param dict subtitle_style: A dictionary specifying the styling options for the subtitles.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response indicating the success or failure of the subtitle addition operation.
        :rtype: AgentResponse
        """
        try:
            if collection_id is None:
                self.videodb_tool = VideoDBTool()
            else:
                self.videodb_tool = VideoDBTool(collection_id=collection_id)

            self.output_message.actions.append(f"Adding subtitles to video {video_id}")
            self.output_message.push_update()

            # Prepare the SubtitleStyle parameters
            if subtitle_style is None:
                subtitle_style = {}
            else:
                # Convert integer values to enum if necessary
                if "border_style" in subtitle_style:
                    border_style_value = subtitle_style["border_style"]
                    border_style_map = {
                        1: SubtitleBorderStyle.no_border,
                        3: SubtitleBorderStyle.opaque_box,
                        4: SubtitleBorderStyle.outline,
                    }
                    subtitle_style["border_style"] = border_style_map.get(
                        border_style_value, SubtitleBorderStyle.outline
                    )

                if "alignment" in subtitle_style:
                    alignment_value = subtitle_style["alignment"]
                    alignment_map = {
                        1: SubtitleAlignment.bottom_left,
                        2: SubtitleAlignment.bottom_center,
                        3: SubtitleAlignment.bottom_right,
                        5: SubtitleAlignment.top_left,
                        6: SubtitleAlignment.top_center,
                        7: SubtitleAlignment.top_right,
                        9: SubtitleAlignment.middle_left,
                        10: SubtitleAlignment.middle_center,
                        11: SubtitleAlignment.middle_right,
                    }
                    subtitle_style["alignment"] = alignment_map.get(
                        alignment_value, SubtitleAlignment.bottom_center
                    )

            # Create SubtitleStyle object
            subtitle_style_obj = SubtitleStyle(**subtitle_style)

            # Add subtitles to the video
            stream_url = self.videodb_tool.add_subtitle(
                video_id=video_id, style=subtitle_style_obj
            )

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent: {e}")
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="Subtitles added successfully",
            data={"stream_url": stream_url},
        )
