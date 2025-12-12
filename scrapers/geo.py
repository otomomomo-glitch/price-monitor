from playwright.sync_api import sync_playwright
from src.parser import extract_text
from src.utils import get_logger

logger = get_logger()

def scrape_geo(url: str) -> dict:
    """Geoの価格情報を取得"""
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
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle")

            price_selectors = [
                "span.goods_detail_price_ b",
                "span.goods_detail_price_small_"
            ]

            price_text = None
            for selector in price_selectors:
                try:
                    page.wait_for_selector(selector, timeout=10000)
                    price_text = extract_text(page, selector)
                    if price_text:
                        break
                except Exception:
                    continue

            if not price_text:
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
