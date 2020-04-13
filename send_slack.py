import json
import os
import requests
import sys

from typing import Dict, Any

Block = Dict[str, str]
Message = Dict[str, Any]


def build_block(type: str, text: str) -> Block:
    return {
        "type": type,
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }

def build_message(filename: str, url: str, channel: str) -> Message:
    ext = os.path.splitext(filename)[1]
    header_text = f"You can download flan report with format *{ext}* below."
    header = build_block(type="section", text=header_text)

    download_text = f"<{url}|{filename}>"
    download = build_block(type="section", text=download_text)

    return {
        "blocks": [header, download],
        "channel": channel,
        "icon_emoji": ":custard:",
        "username": "Flan Scan",
    }

def main(webhook: str, upload: str, filename: str, channel: str):
    bucket = os.getenv("bucket")
    url = ""
    if upload == "aws":
        url = f"https://s3.amazonaws.com/{bucket}/{filename}"
    elif upload == "gcp":
        url = f"https://storage.cloud.google.com/{bucket}/{filename}"

    message = build_message(filename, url, channel)

    response = requests.post(
        webhook, data=json.dumps(message),
        headers={'Content-Type': 'application/json'})
    print(response.status_code, response.reason)

if __name__ == '__main__':
    webhook = os.getenv('slack_webhook')
    channel = os.getenv('slack_channel')
    upload = sys.argv[1]
    filename = sys.argv[2]
    main(webhook, upload, filename, channel)
