import json
import os
from scrapers.rakuten import scrape_rakuten_api
from src.comparator import compare_price
from src.screenshot import take_screenshot
from src.notifier import notify

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCTS_PATH = os.path.join(BASE_DIR, "configs", "products.json")

def main():
    with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    print("--- 楽天市場価格取得開始 ---\n")

    for product in products:
        title = product["title"]
        keyword = title  # API検索用に商品名を使う

        print(f"▶ {title}: {keyword}")

        result = scrape_rakuten_api(keyword)

        if result is None or result.get("price") is None:
            print("❌ 価格取得に失敗しました\n")
            continue

        price = result["price"]
        url = result["url"]

        print(f"タイトル: {result['title']}")
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
