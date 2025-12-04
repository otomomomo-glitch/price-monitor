from playwright.sync_api import sync_playwright
from src.parser import extract_text
from src.utils import get_logger

logger = get_logger()

def scrape_nintendo(url: str) -> dict:
    """Nintendo Store の価格情報を取得"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)

            # 価格セレクタ候補（セール価格と通常価格両方に対応）
            price_selectors = [
                "div[data-testid='PriceBlock_SalePrice'] span.text-4xl",
                "div[data-testid='PriceBlock_BasePrice'] span.text-4xl"
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
                return {"status": "error", "message": "価格の取得に失敗"}

            try:
                price = int(price_text.replace(",", "").replace("円", "").strip())
                logger.info(f"価格取得成功: {price}円 ({url})")
                return {"status": "ok", "price": price}
            except ValueError:
                logger.error(f"価格解析エラー: {price_text} ({url})")
                return {"status": "error", "message": f"価格解析エラー: {price_text}"}

        finally:
            browser.close()


