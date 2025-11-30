import json
import os
from scrapers.nintendo import scrape_nintendo
from src.comparator import compare_price
from src.screenshot import take_screenshot
from src.utils import get_logger

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # price-monitor/
PRODUCTS_PATH = os.path.join(BASE_DIR, "configs", "products.json")
logger = get_logger()

def main():
    with open(PRODUCTS_PATH, "r") as f:
        products = json.load(f)

    print("--- Nintendo スクレイプ開始 ---\n")

    for product in products:
        title = product["title"]
        url = product["url"]
        store_type = product["type"]

        print(f"▶ {title}（{store_type}）: {url}")

        if store_type == "new":
            result = scrape_nintendo(url)
        else:
            print("不明な type です")
            continue

        # ▼ スクレイプ失敗時
        if result is None or result.get("price") is None:
            print("❌ 価格取得に失敗しました\n")
            continue

        print(f"タイトル: {title}")
        print(f"価格: {result['price']}円")
        print(f"URL: {url}\n")



        # -------------------------
        #   比較（±20％チェック）
        # -------------------------

        price = result["price"]

        compare_result = compare_price(url, price)

        status = compare_result["status"]
        message = compare_result["message"]

        from src.notifier import notify

        # ▼ 結果表示
        if status == "error":
            print(f"⚠ 異常検知: {message}\n")

            screenshot_path = take_screenshot(url, title)
            print(f"📷 スクショ保存: {screenshot_path}\n")

            notify(f"異常値を検知しました！\n{title}\n{message}\n{url}", "error")

        elif status == "changed":
            print(f" 価格変動アラート: {message}\n")
            
            screenshot_path = take_screenshot(url, title)
            print(f"📷 スクショ保存: {screenshot_path}\n")

            notify(f"価格変動を検知しました！\n{title}\n{message}\n{url}", "warning")

        elif status == "ok":
            print(f"✓ {message}\n")

        elif status == "test":
            print(f"[TEST] {message}\n")

        else:
            print(f"その他の状態: {message}\n")



logger.info("price-monitor start")
logger.warning("価格が怪しいです")
logger.error("スクショに失敗しました")

if __name__ == "__main__":
    main()
