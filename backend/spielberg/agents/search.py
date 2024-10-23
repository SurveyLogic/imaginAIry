import logging

from spielberg.agents.base import BaseAgent, AgentResponse, AgentStatus
from spielberg.llm.openai import OpenAI
from spielberg.core.session import (
    Session,
    MsgStatus,
    TextContent,
    SearchResultsContent,
    VideoContent,
    VideoData,
    ContextMessage,
    RoleTypes,
)
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)


class SearchAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "search"
        self.description = "Agent to retreive data from VideoDB collections and videos."
        self.llm = OpenAI()
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

    def run(
        self, query: str, collection_id: str, video_id: str = None, *args, **kwargs
    ) -> AgentResponse:
        """
        Retreive data from VideoDB collections and videos.

        :param str query: search query
        :param str video_id: VideoDB videod id.
        :param str collection_id: VideoDB collection id.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response containing search results, text summary and compilation video.
        :rtype: AgentResponse
        """
        try:
            search_result_content = SearchResultsContent(
                status=MsgStatus.progress,
                status_message="Started getting search results.",
                agent_name=self.agent_name,
            )
            self.output_message.content.append(search_result_content)
            compilation_content = VideoContent(
                status=MsgStatus.progress,
                status_message="Started video compilation.",
                agent_name=self.agent_name,
            )
            self.output_message.content.append(compilation_content)
            search_summary_content = TextContent(
                status=MsgStatus.progress,
                status_message="Started generating summary of search results.",
                agent_name=self.agent_name,
            )
            self.output_message.content.append(search_summary_content)
            self.output_message.actions.append("Running search.")
            self.output_message.push_update()
            videodb_tool = VideoDBTool(collection_id=collection_id)
            search_results = videodb_tool.semantic_search(query, video_id)
            shots = search_results.get_shots()
            if not shots:
                search_result_content.status = MsgStatus.error
                search_result_content.status_message = "Failed to get search results."
                compilation_content.status = MsgStatus.error
                compilation_content.status_message = (
                    "Failed to create compilation of search results."
                )
                search_summary_content.status = MsgStatus.error
                search_summary_content.status_message = (
                    "Failed to generate summary of results."
                )
                return AgentResponse(
                    status=AgentStatus.ERROR,
                    message=f"Failed due to no search results found for query {query}",
                    data={
                        "message": f"Failed due to no search results found for query {query}",
                    },
                )
            search_result_videos = {}
            for shot in shots:
                video_id = shot["video_id"]
                video_title = shot["video_title"]
                if video_id in search_result_videos:
                    search_result_videos[video_id]["shots"].append(
                        {
                            "search_score": shot["search_score"],
                            "start": shot["start"],
                            "end": shot["end"],
                            "text": shot["text"],
                        }
                    )
                else:
                    video = videodb_tool.get_video(video_id)
                    search_result_videos[video_id] = {
                        "video_id": video_id,
                        "video_title": video_title,
                        "stream_url": video.get("stream_url"),
                        "duration": video.get("length"),
                        "shots": [
                            {
                                "search_score": shot["search_score"],
                                "start": shot["start"],
                                "end": shot["end"],
                                "text": shot["text"],
                            }
                        ],
                    }
            search_result_content.search_results = list(search_result_videos.values())
            search_result_content.status = MsgStatus.success
            search_result_content.status_message = "Search done."
            self.output_message.actions.append("Generating search result compilation clip..")
            self.output_message.push_update()
            compilation_stream_url = search_results.compile()
            compilation_content.video = VideoData(stream_url=compilation_stream_url)
            compilation_content.status = MsgStatus.success
            compilation_content.status_message = "Compilation done."
            self.output_message.actions.append("Generating search result summary..")
            self.output_message.push_update()
            search_result_text_list = [shot.text for shot in shots]
            search_result_text = "\n\n".join(search_result_text_list)
            search_summary_llm_prompt = f"Summarize the search results for query: {query} search results: {search_result_text}"
            search_summary_llm_message = ContextMessage(
                content=search_summary_llm_prompt, role=RoleTypes.user
            )
            llm_response = self.llm.chat_completions(
                [search_summary_llm_message.to_llm_msg()]
            )
            search_summary_content.text = llm_response.content
            if not llm_response.status:
                search_summary_content.status = MsgStatus.error
                search_summary_content.status_message = (
                    "Failed to generate the summary of search results."
                )
                logger.error(f"LLM failed with {llm_response}")
            else:
                search_summary_content.text = llm_response.content
                search_summary_content.status = MsgStatus.success
                search_summary_content.status_message = (
                    "Here is the summary of search results."
                )
            self.output_message.publish()
        except Exception:
            logger.exception(f"Error in {self.agent_name}.")
            if search_result_content.status != MsgStatus.success:
                search_result_content.status = MsgStatus.error
                search_result_content.status_message = "Failed to get search results."
            elif compilation_content.status != MsgStatus.success:
                compilation_content.status = MsgStatus.error
                compilation_content.status_message = (
                    "Failed to create compilation of search results."
                )
            elif search_summary_content.status != MsgStatus.success:
                search_summary_content.status = MsgStatus.error
                search_summary_content.status_message = (
                    "Failed to generate summary of results."
                )
            return AgentResponse(
                status=AgentStatus.ERROR, message="Failed the search with exception."
            )
        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="Search done and showed above to user.",
            data={"message": "Search done.", "stream_link": compilation_stream_url},
        )
