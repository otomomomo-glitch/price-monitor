import pytest
from src import comparator

def test_initial_registration(tmp_path, monkeypatch):
    # 履歴ファイルを一時ディレクトリに差し替え
    monkeypatch.setattr(comparator, "HISTORY_PATH", tmp_path / "price_history.json")

    result = comparator.compare_price("test_product", 1000)
    assert result["status"] == "ok"
    assert "初回登録" in result["message"]

def test_price_change(tmp_path, monkeypatch):
    monkeypatch.setattr(comparator, "HISTORY_PATH", tmp_path / "price_history.json")
    # 初回登録
    comparator.compare_price("test_product", 1000)
    # 20%以上の変動
    result = comparator.compare_price("test_product", 2000)
    assert result["status"] == "changed"
    assert "価格変動" in result["message"]

def test_no_change(tmp_path, monkeypatch):
    monkeypatch.setattr(comparator, "HISTORY_PATH", tmp_path / "price_history.json")
    comparator.compare_price("test_product", 1000)
    result = comparator.compare_price("test_product", 1050)  # 5%変動
    assert result["status"] == "ok"
    assert "変動なし" in result["message"]

def test_anomaly_detection():
    assert comparator.detect_anomaly(None) is not None
    assert comparator.detect_anomaly(0) is not None
    assert comparator.detect_anomaly(999999) is not None
    assert comparator.detect_anomaly(1000) is None
