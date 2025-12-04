import json
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "configs", "settings.json")

# 設定ファイルがあれば読み込む
if os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        SETTINGS = json.load(f)
else:
    SETTINGS = {}


def notify_slack(message: str) -> bool:
    """Slackへメッセージ通知"""
    # settings.json または環境変数から取得
    url = SETTINGS.get("slack_webhook_url") or os.getenv("SLACK_WEBHOOK_URL")

    if not url:
        print("⚠ Slack Webhook URL が設定されていません")
        return False

    payload = {"text": message}

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"⚠ Slack通知失敗: {response.status_code} {response.text}")
            return False
        return True
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
    return notify_slack(full_message)
