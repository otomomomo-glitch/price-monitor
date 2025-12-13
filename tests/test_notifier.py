import pytest
from src import notifier

def test_notify_called(monkeypatch):
    called = {}

    def mock_post(url, json):
        called["url"] = url
        called["json"] = json
        class MockResponse:
            status_code = 200
        return MockResponse()

    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://dummy-webhook")
    monkeypatch.setattr("requests.post", mock_post)

    notifier.notify("テストメッセージ", level="info")

    assert "url" in called
    assert "json" in called
    # メッセージが「ℹ️ 情報」で始まり、本文に「テストメッセージ」が含まれることを確認
    assert called["json"]["text"].startswith("ℹ️ 情報")
    assert "テストメッセージ" in called["json"]["text"]
