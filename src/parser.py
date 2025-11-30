# src/parser.py

import re


def extract_text(page, selector: str) -> str:
    locator = page.locator(selector)
    return locator.first.inner_text().strip()


def extract_price(text: str) -> int:
    numbers = re.findall(r"\d+", text)
    return int("".join(numbers)) if numbers else None
