import os
import requests
from src.utils import get_logger

logger = get_logger()

def scrape_rakuten_api(keyword, hits=5):
    app_id = os.getenv("RAKUTEN_APP_ID")  # ←関数内で毎回取得
    if not app_id:
        logger.error("楽天APIのアプリケーションIDが設定されていません")
        return []

    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
    params = {"applicationId": app_id, "keyword": keyword, "hits": hits}
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        items = data.get("Items", [])
        results = []
        for entry in items:
            item = entry["Item"]
            results.append({
                "title": item["itemName"],
                "price": item["itemPrice"],
                "url": item["itemUrl"],
                "shipping": "送料別" if item.get("postageFlag") else "",
                "total": item["itemPrice"] + (0 if item.get("postageFlag") == 0 else 1)
            })
        return results
    except Exception as e:
        logger.error(f"楽天API呼び出しエラー: {e}")
        return []
