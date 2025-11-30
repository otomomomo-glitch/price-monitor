import json
import os
from src.utils import get_logger

# -------------------------------------
# ロガーの初期化
# -------------------------------------
logger = get_logger(__name__)

# -------------------------------------
# ファイルパス
# -------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_PATH = os.path.join(BASE_DIR, "configs", "price_history.json")


# -------------------------------------
# 価格履歴の読み書き
# -------------------------------------

def load_history():
    """過去価格データを読み込む"""
    if not os.path.exists(HISTORY_PATH):
        logger.debug(f"価格履歴ファイルが存在しません: {HISTORY_PATH}")
        return {}

    try:
        with open(HISTORY_PATH, "r") as f:
            data = json.load(f)
            logger.debug("価格履歴を読み込みました")
            return data
    except Exception as e:
        logger.error(f"価格履歴の読み込みに失敗しました: {e}")
        return {}


def save_history(history):
    """過去価格データを保存"""
    try:
        with open(HISTORY_PATH, "w") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        logger.debug("価格履歴を保存しました")
    except Exception as e:
        logger.error(f"価格履歴の保存に失敗しました: {e}")


# -------------------------------------
# 異常値チェックロジック
# -------------------------------------

def detect_anomaly(price):
    """
    異常値を検知する（None・異常に安い・異常に高い）
    """
    if price is None:
        logger.warning("価格取得に失敗（price=None）")
        return "価格が取得できませんでした"

    if price <= 1:
        logger.warning(f"価格が異常に低いです: {price}円")
        return f"価格が異常に低いです（{price}円）"

    if price > 200_000:
        logger.warning(f"価格が異常に高いです: {price}円")
        return f"価格が異常に高いです（{price}円）"

    return None


# -------------------------------------
# 価格比較メインロジック
# -------------------------------------

def compare_price(product_id, new_price, test_mode=False):
    """
    価格比較のメイン関数。ログ出力を強化済み。

    戻り値：
    {
        "status": "ok" | "changed" | "error" | "test",
        "message": str
    }
    """
    logger.info(f"[START] product={product_id}, new_price={new_price}")

    # ▼ 異常値チェック
    anomaly = detect_anomaly(new_price)
    if anomaly:
        return {"status": "error", "message": anomaly}

    history = load_history()
    old_price = history.get(product_id)

    # ▼ テストモード
    if test_mode:
        msg = f"[TEST] old={old_price}, new={new_price}"
        logger.debug(msg)
        return {"status": "test", "message": msg}

    # ▼ 初回データ
    if old_price is None:
        logger.info(f"初回登録: {product_id} → {new_price}円")
        history[product_id] = new_price
        save_history(history)
        return {"status": "ok", "message": "初回登録しました"}

    # ▼ 変動率
    diff_ratio = abs(new_price - old_price) / old_price
    logger.debug(f"変動率: {diff_ratio*100:.1f}%")

    if diff_ratio >= 0.20:
        msg = f"価格変動！ {old_price}円 → {new_price}円（{diff_ratio*100:.1f}%）"
        logger.info(msg)
        history[product_id] = new_price
        save_history(history)
        return {"status": "changed", "message": msg}

    # ▼ 変動なし
    msg = f"変動なし（前回: {old_price}円 / 今回: {new_price}円）"
    logger.info(msg)
    return {"status": "ok", "message": msg}
