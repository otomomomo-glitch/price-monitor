import requests
from src.utils import get_logger

logger = get_logger()

RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APPLICATION_ID = "1046951952480833102"  # ←取得したアプリケーションIDをここに設定

def scrape_rakuten_api(keyword: str, hits: int = 1) -> dict:
    """
    楽天市場APIを叩いて商品価格を取得する関数
    :param keyword: 商品名や検索キーワード
    :param hits: 取得件数（デフォルト1件）
    :return: {"status": "ok", "title": 商品名, "price": 価格, "url": 商品URL}
    """
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
            return {"status": "error", "message": "商品が見つかりませんでした"}

        item = data["Items"][0]["Item"]
        title = item["itemName"]
        price = item["itemPrice"]
        url = item["itemUrl"]

        logger.info(f"価格取得成功: {price}円 ({title})")
        return {"status": "ok", "title": title, "price": price, "url": url}

    except Exception as e:
        logger.error(f"楽天APIエラー: {e}")
        return {"status": "error", "message": str(e)}
