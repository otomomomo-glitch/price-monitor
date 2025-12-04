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

            # 価格セレクタ（将来変更に備えて複数候補を用意しても良い）
            price_selector = "div[data-testid='PriceBlock_SalePrice'] span.text-4xl"

            price_text = extract_text(page, price_selector)

            if not price_text:
                logger.warning(f"価格取得失敗: {url}")
                return {"status": "error", "message": "価格の取得に失敗"}

            try:
                price = int(price_text.replace(",", ""))
                logger.info(f"価格取得成功: {price}円 ({url})")
                return {"status": "ok", "price": price}
            except ValueError:
                logger.error(f"価格解析エラー: {price_text} ({url})")
                return {"status": "error", "message": f"価格解析エラー: {price_text}"}

        finally:
            browser.close()

