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

    monkeypatch.setattr("requests.post", mock_post)

    notifier.notify("テストメッセージ", level="info")

    assert "url" in called
    assert "json" in called
    assert called["json"]["text"].startswith("テストメッセージ")
