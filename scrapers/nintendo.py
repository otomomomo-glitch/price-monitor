from playwright.sync_api import sync_playwright
from src.parser import extract_text
from src.utils import get_logger

logger = get_logger()

def scrape_nintendo(url: str) -> dict:
    """任天堂ストアの価格情報を取得"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            locale="ja-JP",
            extra_http_headers={
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
                "Referer": "https://www.google.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        )
        page = context.new_page()
        try:
            # DOM構築完了まで待つ
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # 価格要素を直接待つ
            try:
                page.wait_for_selector("span.price", timeout=10000)
                price_text = extract_text(page, "span.price")
            except Exception:
                logger.warning(f"価格取得失敗: {url}")
                logger.debug(f"Page content dump:\n{page.content()[:1000]}")
                return {"status": "error", "message": "価格の取得に失敗"}

            try:
                price = int(price_text.replace(",", "").replace("円", "").strip())
                logger.info(f"価格取得成功: {price}円 ({url})")
                return {"status": "ok", "price": price}
            except ValueError:
                logger.error(f"価格解析エラー: {price_text} ({url})")
                logger.debug(f"Page content dump:\n{page.content()[:1000]}")
                return {"status": "error", "message": f"価格解析エラー: {price_text}"}

        finally:
            browser.close()


