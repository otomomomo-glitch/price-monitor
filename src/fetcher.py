from playwright.sync_api import sync_playwright

def get_page(url: str):
    """
    Playwright でページを開いて返す
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    return page
