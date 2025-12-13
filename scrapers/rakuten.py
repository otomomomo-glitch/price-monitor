import os
import requests
from src.utils import get_logger
from dotenv import load_dotenv

logger = get_logger()

load_dotenv()  # ローカル開発時に .env を読み込む

RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APPLICATION_ID = os.getenv("RAKUTEN_APP_ID")

def scrape_rakuten_api(keyword: str, hits: int = 5) -> list:
    if not APPLICATION_ID:
        logger.error("楽天APIのアプリケーションIDが設定されていません")
        return []

    params = {
        "applicationId": APPLICATION_ID,
        "keyword": keyword,
        "hits": hits,
        "format": "json"
    }

    try:
        response = requests.get(RAKUTEN_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "Items" not in data or len(data["Items"]) == 0:
            logger.warning(f"商品が見つかりませんでした: {keyword}")
            return []

        results = []
        for entry in data["Items"]:
            item = entry["Item"]
            title = item["itemName"]
            price = item["itemPrice"]
            url = item["itemUrl"]

            postage_flag = item.get("postageFlag", 0)
            if postage_flag == 0:
                shipping = None
                total = price
            else:
                shipping = "送料別"
                # 送料額はAPIで取れないので、同価格なら送料無料を優先するために +1 する
                total = price + 1  

            results.append({
                "title": title,
                "price": price,
                "shipping": shipping,
                "total": total,
                "url": url
            })

        return results

    except Exception as e:
        logger.error(f"楽天APIエラー: {e}")
        return []
