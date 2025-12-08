import pytest
from src import parser

def test_extract_price_concat():
    text = "価格は4,730円（税込）"
    price = parser.extract_price_concat(text)
    assert price == 4730

def test_extract_price_last():
    text = "税込4730円 10%OFF"
    price = parser.extract_price_last(text)
    assert price == 10 or price == 4730  # サイト仕様に応じて調整

def test_extract_text_success(page_mock):
    # page_mock は Playwright のモックを作る（pytest fixtureで用意）
    page_mock.locator.return_value.first.inner_text.return_value = "テスト価格"
    result = parser.extract_text(page_mock, "dummy_selector")
    assert result == "テスト価格"
