import json
import os
from scrapers.nintendo import scrape_nintendo
from .comparator import compare_price
from .screenshot import take_screenshot
from .notifier import notify

# プロジェクトのルートディレクトリを基準にする
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # price-monitor/
PRODUCTS_PATH = os.path.join(BASE_DIR, "configs", "products.json")


def main():
    # 商品リストを読み込み
    with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    print("--- 商品スクレイプ開始 ---\n")

    for product in products:
        title = product["title"]
        url = product["url"]
        store_type = product["type"]

        print(f"▶ {title}（{store_type}）: {url}")

        # ストアタイプごとにスクレイプ処理を分岐
        if store_type == "new":
            result = scrape_nintendo(url)
        else:
            print("❌ 未対応の type です\n")
            continue

        # ▼ スクレイプ失敗時
        if result is None or result.get("price") is None:
            print("❌ 価格取得に失敗しました\n")
            continue

        price = result["price"]

        print(f"タイトル: {title}")
        print(f"価格: {price}円")
        print(f"URL: {url}\n")

        # -------------------------
        #        比較処理
        # -------------------------
        compare_result = compare_price(url, price)

        status = compare_result["status"]
        message = compare_result["message"]

        # ▼ 結果表示とアクション
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

