import json
import os
from scrapers.nintendo import scrape_nintendo
from scrapers.rakuten import scrape_rakuten
from src.comparator import compare_price
from src.screenshot import take_screenshot
from src.notifier import notify

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCTS_PATH = os.path.join(BASE_DIR, "configs", "products.json")

SCRAPERS = {
    "nintendo": scrape_nintendo,
    "rakuten": scrape_rakuten,
}

def main():
    with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    print("--- 商品スクレイプ開始 ---\n")

    for product in products:
        title = product["title"]
        url = product["url"]
        store = product.get("store")

        print(f"▶ {title}（{store}）: {url}")

        scraper = SCRAPERS.get(store)
        if not scraper:
            print("❌ 未対応の store です\n")
            continue

        result = scraper(url)

        if result is None or result.get("price") is None:
            print("❌ 価格取得に失敗しました\n")
            continue

        price = result["price"]

        print(f"タイトル: {title}")
        print(f"価格: {price}円")
        print(f"URL: {url}\n")

        compare_result = compare_price(url, price)
        status = compare_result["status"]
        message = compare_result["message"]

        if status == "error":
            print(f"⚠ 異常検知: {message}")
            notify(f"⚠ 異常検知: {message}", level="error")
            screenshot_path = take_screenshot(url, title)
            print(f"📷 スクショ保存: {screenshot_path}\n")

        elif status == "changed":
            print(f"📢 価格変動アラート: {message}\n")
            notify(f"📢 価格変動アラート: {message}", level="warning")

        elif status == "ok":
            print(f"✓ {message}\n")

        elif status == "test":
            print(f"[TEST] {message}\n")

        else:
            print(f"その他の状態: {message}\n")


if __name__ == "__main__":
    main()
