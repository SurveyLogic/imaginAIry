import os

from flask import current_app as app
from flask_socketio import Namespace

from spielberg.db import load_db
from spielberg.handler import ChatHandler


class ChatNamespace(Namespace):
    def on_chat(self, message):
        chat_handler = ChatHandler(
            db=load_db(os.getenv("SERVER_DB_TYPE", app.config["DB_TYPE"]))
        )
        chat_handler.chat(message)
