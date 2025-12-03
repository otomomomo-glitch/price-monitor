# src/notifier.py

import json
import os
import requests

# Settingsファイル読込
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "configs", "settings.json")

with open(SETTINGS_PATH, "r") as f:
    SETTINGS = json.load(f)


def notify_slack(message: str) -> bool:
    """Slackへメッセージ通知"""
    url = SETTINGS.get("slack_webhook_url")

    if not url:
        print("⚠ Slack Webhook URL が設定されていません")
        return False

    payload = {"text": message}

    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠ Slack通知失敗: {e}")
        return False


def notify(message: str, level: str = "info"):
    """
    共通通知関数（将来メールやTeamsもここに統合）
    level: info / warning / error
    """

    header = {
        "warning": "⚠️ 警告",
        "error": "❌ エラー"
    }.get(level, "ℹ️ 情報")

    full_message = f"{header}\n{message}"

    # Slackのみ実装（拡張しやすい形にしてある）
    return notify_slack(full_message)
