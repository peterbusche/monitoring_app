# notifications.py
import requests
from monitoring_app.db import DISCORD_WEBHOOK_URL


def send_discord_alert(url, status_code):

    # potentially get more embed info for notification
    payload = {"content": f"ALERT: {url} returned {status_code}\n"}

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    if response.status_code != 204:  # 204 = no content (discord's success response)
        print(
            f"Failed to send Discord alert. Code: {response.status_code}, Response: {response.text}"
        )
    else:
        print(f"Sent Discord alert for {url} with status code {status_code}")
