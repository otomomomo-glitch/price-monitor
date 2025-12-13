import logging
import sys

def get_logger(name: str = "price-monitor") -> logging.Logger:
    """
    プロジェクト全体で共通して使えるロガーを返す。
    ログレベルやフォーマットはここで統一する。
    """
    logger = logging.getLogger(name)

    if not logger.handlers:  # 二重追加防止
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
