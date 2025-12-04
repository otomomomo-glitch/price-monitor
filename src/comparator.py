import json
import os
from src.utils import get_logger

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_PATH = os.path.join(BASE_DIR, "configs", "price_history.json")

logger = get_logger()

# -------------------------
# 価格履歴の読み書き
# -------------------------

def load_history():
    """過去価格データを読み込む"""
    if not os.path.exists(HISTORY_PATH):
        return {}
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history):
    """過去価格データを保存"""
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


# -------------------------
# 異常値チェックロジック
# -------------------------

def detect_anomaly(price):
    """
    異常値を検知する
      - 取得失敗: None
      - 0円 / 1円など異常に安い
      - 数百万など異常に高い
    """
    if price is None:
        return "価格が取得できませんでした"

    if price <= 1:
        return f"価格が異常に低いです（{price}円）"

    if price > 200_000:
        return f"価格が異常に高いです（{price}円）"

    return None  # 問題なし


# -------------------------
# 通常の比較ロジック（ログ統合版）
# -------------------------

def compare_price(product_id, new_price, test_mode=False):
    """
    価格を比較し、変動が大きい場合に報告する。
    test_mode=True の場合、比較結果を強制的に返す（動作確認用）

    戻り値：
        {
            "status": "ok" | "changed" | "error" | "test",
            "message": str
        }
    """

    logger.debug(f"Compare start: product_id={product_id}, new_price={new_price}")

    # ▼ 異常値チェック
    anomaly = detect_anomaly(new_price)
    if anomaly:
        logger.warning(f"Anomaly detected: {anomaly}")
        return {"status": "error", "message": anomaly}

    history = load_history()
    old_price = history.get(product_id)

    # ▼ テストモードの場合
    if test_mode:
        logger.info(f"Test mode: old={old_price}, new={new_price}")
        return {
            "status": "test",
            "message": f"[TEST] old={old_price}, new={new_price}"
        }

    # ▼ 初回データ
    if old_price is None:
        history[product_id] = new_price
        save_history(history)
        logger.info(f"Initial registration: {new_price}円")
        return {"status": "ok", "message": "初回登録しました"}

    # ▼ 変動率を計算
    diff_ratio = abs(new_price - old_price) / old_price
    logger.debug(f"Diff ratio={diff_ratio:.2f} (old={old_price}, new={new_price})")

    if diff_ratio >= 0.20:
        history[product_id] = new_price
        save_history(history)
        logger.info(f"Price changed: {old_price}円 → {new_price}円")
        return {
            "status": "changed",
            "message": f"価格変動！ {old_price}円 → {new_price}円（変動率：{diff_ratio*100:.1f}%）"
        }

    # ▼ 変動なし
    logger.info(f"No change: old={old_price}, new={new_price}")
    return {
        "status": "ok",
        "message": f"変動なし（前回: {old_price}円 / 今回: {new_price}円）"
    }
