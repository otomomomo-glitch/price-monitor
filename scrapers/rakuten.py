import requests
from src.utils import get_logger

logger = get_logger()

RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APPLICATION_ID = "YOUR_APPLICATION_ID"  # ←取得したアプリケーションIDを設定

def scrape_rakuten_api(keyword: str, hits: int = 5) -> list:
    """
    楽天市場APIを叩いて複数候補の商品価格を取得
    :param keyword: 商品名や検索キーワード
    :param hits: 取得件数（デフォルト5件）
    :return: [{"title": 商品名, "price": 価格, "shipping": 送料情報, "total": 合計, "url": 商品URL}, ...]
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
            return []

        results = []
        for entry in data["Items"]:
            item = entry["Item"]
            title = item["itemName"]
            price = item["itemPrice"]
            url = item["itemUrl"]

            # 送料フラグ: 0=送料無料, 1=送料別
            postage_flag = item.get("postageFlag", 0)
            if postage_flag == 0:
                shipping = None
                total = price
            else:
                # 送料別 → 合計は「価格＋送料」だが、送料額はAPIでは詳細が取れないことが多い
                # ここでは「送料別」と明示し、totalはpriceのままにする
                shipping = "送料別"
                total = price

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
