import pytest
import scrapers.rakuten_api as rakuten

def test_scrape_rakuten_api_success(monkeypatch):
    # ダミーの楽天APIキーを設定
    monkeypatch.setenv("RAKUTEN_APP_ID", "dummy_app_id")

    # モックレスポンス
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self):
                return {
                    "Items": [
                        {"Item": {
                            "itemName": "テスト商品",
                            "itemPrice": 1000,
                            "itemUrl": "http://example.com",
                            "postageFlag": 0
                        }}
                    ]
                }
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    results = rakuten.scrape_rakuten_api("テスト商品")
    assert len(results) == 1
    assert results[0]["title"] == "テスト商品"
    assert results[0]["total"] == 1000
