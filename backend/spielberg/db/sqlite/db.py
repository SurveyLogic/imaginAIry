import json
import sqlite3
import time

from typing import List

from spielberg.constants import DBType
from spielberg.db.base import BaseDB


class SQLiteDB(BaseDB):
    def __init__(self, db_path: str = "spielberg.db"):
        self.db_type = DBType.SQLITE
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=True)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        print("Connected to SQLite DB...")

    def create_session(
        self,
        session_id: str,
        video_id: str,
        collection_id: str,
        created_at: int = None,
        updated_at: int = None,
        metadata: dict = {},
        **kwargs,
    ) -> None:
        created_at = created_at or int(time.time())
        updated_at = updated_at or int(time.time())

        self.cursor.execute(
            """
        INSERT OR IGNORE INTO sessions (session_id, video_id, collection_id, created_at, updated_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                session_id,
                video_id,
                collection_id,
                created_at,
                updated_at,
                json.dumps(metadata),
            ),
        )
        self.conn.commit()

    def get_session(self, session_id: str) -> dict:
        self.cursor.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        )
        row = self.cursor.fetchone()
        if row is not None:
            session = dict(row)  # Convert sqlite3.Row to dictionary
            session["metadata"] = json.loads(session["metadata"])
            return session

        else:
            return {}  # Return an empty dictionary if no data found

    def get_sessions(self) -> list:
        self.cursor.execute("SELECT * FROM sessions ORDER BY updated_at DESC")
        row = self.cursor.fetchall()
        sessions = [dict(r) for r in row]
        for s in sessions:
            s["metadata"] = json.loads(s["metadata"])
        return sessions

    def add_or_update_msg_to_conv(
        self,
        session_id: str,
        conv_id: str,
        msg_id: str,
        msg_type: str,
        agents: List[str],
        actions: List[str],
        content: List[dict],
        status: str = None,
        created_at: int = None,
        updated_at: int = None,
        metadata: dict = {},
        **kwargs,
    ) -> None:
        created_at = created_at or int(time.time())
        updated_at = updated_at or int(time.time())

        self.cursor.execute(
            """
        INSERT OR REPLACE INTO conversations (session_id, conv_id, msg_id, msg_type, agents, actions, content, status, created_at, updated_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                session_id,
                conv_id,
                msg_id,
                msg_type,
                json.dumps(agents),
                json.dumps(actions),
                json.dumps(content),
                status,
                created_at,
                updated_at,
                json.dumps(metadata),
            ),
        )
        self.conn.commit()

    def get_conversations(self, session_id: str) -> list:
        self.cursor.execute(
            "SELECT * FROM conversations WHERE session_id = ?", (session_id,)
        )
        rows = self.cursor.fetchall()
        conversations = []
        for row in rows:
            if row is not None:
                conv_dict = dict(row)
                conv_dict["agents"] = json.loads(conv_dict["agents"])
                conv_dict["actions"] = json.loads(conv_dict["actions"])
                conv_dict["content"] = json.loads(conv_dict["content"])
                conv_dict["metadata"] = json.loads(conv_dict["metadata"])
                conversations.append(conv_dict)
        return conversations

    def get_context_messages(self, session_id: str) -> list:
        self.cursor.execute(
            "SELECT context_data FROM context_messages WHERE session_id = ?",
            (session_id,),
        )
        result = self.cursor.fetchone()
        return json.loads(result[0]) if result else {}

    def add_or_update_context_msg(
        self,
        session_id: str,
        context_messages: list,
        created_at: int = None,
        updated_at: int = None,
        metadata: dict = {},
        **kwargs,
    ) -> None:
        created_at = created_at or int(time.time())
        updated_at = updated_at or int(time.time())

        self.cursor.execute(
            """
        INSERT OR REPLACE INTO context_messages (context_data, session_id, created_at, updated_at, metadata)
        VALUES (?, ?, ?, ?, ?)
        """,
            (
                json.dumps(context_messages),
                session_id,
                created_at,
                updated_at,
                json.dumps(metadata),
            ),
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
