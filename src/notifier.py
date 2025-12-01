import os
import requests

def notify_slack(message: str):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ SLACK_WEBHOOK_URL が設定されていません")
        return
    
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Slack通知失敗: {response.text}")
    except Exception as e:
        print(f"Slack通知中にエラー: {e}")
