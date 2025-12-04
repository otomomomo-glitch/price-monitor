from playwright.sync_api import sync_playwright

def fetch_html(url: str) -> str:
    """指定URLのHTMLを返す"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        html = page.content()
        browser.close()
    return html
