import re


def extract_price(page, selector: str) -> str:
    locator = page.locator(selector)
    return locator.first.inner_text().strip()


def extract_price_concat(text: str) -> int:
    numbers = re.findall(r"\d+", text)
    return int("".join(numbers)) if numbers else None

def extract_price_last(text: str) -> int:
    numbers = re.findall(r"\d+", text)
    return int(numbers[-1]) if numbers else None

def extract_text(page, selector: str) -> str:
    try:
        locator = page.locator(selector)
        return locator.first.inner_text().strip()
    except Exception:
        return None

