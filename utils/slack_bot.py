import os
import slack_sdk
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

slack_web_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

# specify the channel and the message
channel_id = "papers-with-code"

def send_to_slack(content):
  message = content
  # send a message
  response = slack_web_client.chat_postMessage(
    channel=channel_id,
    text=message
  )