import os
import re
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
import nest_asyncio
import subprocess
import platform

# async イベントループ二重起動対応
nest_asyncio.apply()


def sanitize_filename(name: str) -> str:
    """ファイル名に使えない文字を除去"""
    return re.sub(r'[\\/*?:"<>|]', "_", name)


async def _async_take_screenshot(url: str, title: str) -> str:
    """スクリーンショットを非同期で撮影"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    screenshot_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    safe_title = sanitize_filename(title)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(screenshot_dir, f"{safe_title}_{timestamp}.png")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        await page.screenshot(path=filepath, full_page=True)
        await browser.close()

    return filepath


def open_file(path: str):
    """OSに応じてスクリーンショットを自動で開く"""
    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["open", path])
        elif os_name == "Windows":  # Windows
            os.startfile(path)
        else:  # Linux
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print(f"⚠ スクショ自動オープン失敗: {e}")


def take_screenshot(url: str, title: str) -> str:
    """同期関数として呼び出し可能"""
    try:
        filepath = asyncio.run(_async_take_screenshot(url, title))
    except RuntimeError:
        # 既存ループがある場合は nest_asyncio で対応済み
        loop = asyncio.get_event_loop()
        filepath = loop.run_until_complete(_async_take_screenshot(url, title))

    # CI環境では自動オープンしない
    if os.getenv("CI") != "true":
        open_file(filepath)

    return filepath



    # スクショを自動で開く
    if os.getenv("CI") != "true":
        open_file(filepath)

        return filepath

