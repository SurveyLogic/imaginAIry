import os
import logging

from spielberg.agents.thumbnail import ThumbnailAgent
from spielberg.agents.summary import SummaryAgent
from spielberg.agents.download import DownloadAgent
from spielberg.agents.pricing import PricingAgent
from spielberg.agents.upload import UploadAgent
from spielberg.agents.search import SearchAgent
from spielberg.agents.brandkit import BrandkitAgent
from spielberg.agents.profanity_remover import ProfanityRemoverAgent

from spielberg.core.session import Session, InputMessage, MsgStatus
from spielberg.core.reasoning import ReasoningEngine
from spielberg.db.base import BaseDB
from spielberg.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)


class ChatHandler:
    def __init__(self, db, **kwargs):
        self.db = db

        # Register the agents here
        self.agents = [
            ThumbnailAgent,
            SummaryAgent,
            DownloadAgent,
            PricingAgent,
            UploadAgent,
            SearchAgent,
            BrandkitAgent,
            ProfanityRemoverAgent,
        ]

    def add_videodb_state(self, session):
        from videodb import connect

        session.state["conn"] = connect(
            base_url=os.getenv("VIDEO_DB_BASE_URL", "https://api.videodb.io")
        )
        session.state["collection"] = session.state["conn"].get_collection(
            session.collection_id
        )
        if session.video_id:
            session.state["video"] = session.state["collection"].get_video(
                session.video_id
            )
        logger.info("videodb state added to session")

    def agents_list(self):
        return [
            {
                "name": agent_instance.name,
                "description": agent_instance.agent_description,
            }
            for agent in self.agents
            for agent_instance in [agent(Session(db=self.db))]
        ]

    def chat(self, message):
        logger.info(f"ChatHandler input message: {message}")

        session = Session(db=self.db, **message)
        session.create()
        input_message = InputMessage(db=self.db, **message)
        input_message.publish()

        try:
            self.add_videodb_state(session)
            agents = [agent(session=session) for agent in self.agents]
            agents_mapping = {agent.name: agent for agent in agents}

            res_eng = ReasoningEngine(input_message=input_message, session=session)
            if input_message.agents:
                for agent_name in input_message.agents:
                    res_eng.register_agents([agents_mapping[agent_name]])
            else:
                res_eng.register_agents(agents)

            res_eng.run()

        except Exception as e:
            session.output_message.update_status(MsgStatus.error)
            logger.exception(f"Error in chat handler: {e}")


class SessionHandler:
    def __init__(self, db: BaseDB, **kwargs):
        self.db = db

    def get_session(self, session_id):
        session = Session(db=self.db, session_id=session_id)
        return session.get()

    def get_sessions(self):
        session = Session(db=self.db)
        return session.get_all()


class VideoDBHandler:
    def __init__(self, collection_id):
        self.videodb_tool = VideoDBTool(collection_id=collection_id)

    def get_collection(self):
        """Get a collection by ID."""
        return self.videodb_tool.get_collection()

    def get_collections(self):
        """Get all collections."""
        return self.videodb_tool.get_collections()

    def get_video(self, video_id):
        """Get a video by ID."""
        return self.videodb_tool.get_video(video_id)

    def get_videos(self):
        """Get all videos in a collection."""
        return self.videodb_tool.get_videos()
