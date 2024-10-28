import os

from slack_sdk import WebClient


def send_message_to_channel(message, channel_name):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_client = WebClient(token=slack_token)
    response = slack_client.chat_postMessage(channel=channel_name, text=message)
    return response
