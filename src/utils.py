import logging
import os
from logging.handlers import RotatingFileHandler

# ログディレクトリが存在しない場合は作成
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")


class ColorFormatter(logging.Formatter):
    """
    ターミナル出力時に色付きログをサポート
    """
    COLORS = {
        "DEBUG": "\033[94m",   # 青
        "INFO": "\033[92m",    # 緑
        "WARNING": "\033[93m", # 黄
        "ERROR": "\033[91m",   # 赤
        "CRITICAL": "\033[95m" # マゼンタ
    }
    RESET = "\033[0m"

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, '')}[%(levelname)s]%(message)s{self.RESET}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name: str = "app"):
    """
    共通 logger を生成して返す。
    import したどこからでも同じ logger を取得できる。
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        # すでに設定済みならそのまま返す
        return logger

    logger.setLevel(logging.DEBUG)

    # --- ファイルログ（ローテーションあり） ---
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    # --- コンソールログ（色付き） ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())

    # logger に追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
