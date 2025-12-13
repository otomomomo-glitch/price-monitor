import json
import os
from scrapers.rakuten import scrape_rakuten_api
from src.notifier import notify

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCTS_PATH = os.path.join(BASE_DIR, "configs", "products.json")

def main():
    products = [
        {"title": "タイオン ダウンマフラー"},
        {"title": "エビオス錠 2000錠"}
    ]

    print("--- 楽天市場価格取得開始 ---\n")

    for product in products:
        title = product["title"]
        keyword = title

        print(f"▶ {title}: {keyword}")

        results = scrape_rakuten_api(keyword, hits=5)

        if not results:
            print("❌ 商品が見つかりませんでした\n")
            continue

        # 安い順に並べ替え（totalを基準）
        sorted_results = sorted(results, key=lambda x: x["total"])

        message_lines = [f"【{title}】の価格一覧（安い順）"]
        for item in sorted_results:
            shipping_info = f" + {item['shipping']}" if item['shipping'] else ""
            line = f"- {item['price']}円{shipping_info} | {item['url']}"
            message_lines.append(line)

        message = "\n".join(message_lines)
        print(message + "\n")
        # コンソール出力
        print(message + "\n")

        # Slackなどに通知
        notify(message, level="info")

if __name__ == "__main__":
    main()
