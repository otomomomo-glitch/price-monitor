# scrapers/nintendo.py

from playwright.sync_api import sync_playwright
from src.parser import extract_text
from src.utils import get_logger

logger = get_logger()

def scrape_nintendo(url: str) -> dict:
    """Nintendo Store の価格情報を取得"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)

        # ここは前回修正したセレクタを使う
        price_selector = "div[data-testid='PriceBlock_SalePrice'] span.text-4xl"

        price_text = extract_text(page, price_selector)
        browser.close()

        if not price_text:
            return {"status": "error", "message": "価格の取得に失敗"}

        try:
            price = int(price_text.replace(",", ""))
        except ValueError:
            return {"status": "error", "message": f"価格解析エラー: {price_text}"}

        return {"status": "ok", "price": price}
