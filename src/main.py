from .fetcher import get_page
from .parser import parse_price
from .comparator import detect_price_change
from .notifier import notify_slack
from .utils import load_products, load_settings

def main():
    print("=== Price Monitor Started ===")

    products = load_products()
    settings = load_settings()

    for p in products:
        url = p["url"]
        name = p["name"]
        old_price = p.get("last_price")

        print(f"Checking: {name}")

        html = fetch_html(url)
        new_price = parse_price(html)

        if new_price is None:
            notify_slack(f":warning: {name} の価格を取得できませんでした。")
            continue

        result = detect_price_change(old_price, new_price, settings["threshold_percent"])

        # 変化あり → Slack通知
        if result["changed"]:
            msg = (
                f":warning: 価格変動を検知しました！\n"
                f"{name}\n"
                f"価格変動！ {old_price}円 → {new_price}円（変動率：{result['diff_percent']}%）\n"
                f"{url}"
            )
            notify_slack(msg)

        # JSON に最新の価格を書き戻す
        p["last_price"] = new_price

    print("=== Price Monitor Finished ===")

if __name__ == "__main__":
    main()
