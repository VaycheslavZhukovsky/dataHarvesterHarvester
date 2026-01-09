import logging
from logging.handlers import RotatingFileHandler  # <<< ДОБАВЛЕНО


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[41m", # Red background
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        formatter = logging.Formatter(log_fmt)
        message = formatter.format(record)
        color = self.COLORS.get(record.levelno, self.RESET)
        return f"{color}{message}{self.RESET}"


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)   # <<< ИЗМЕНЕНО

    # -----------------------------
    # Консольный обработчик
    # -----------------------------
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)       # <<< ИЗМЕНЕНО
    ch.setFormatter(ColorFormatter())

    # -----------------------------
    # Файловый обработчик
    # -----------------------------
    fh = RotatingFileHandler(
        filename="app.log",            # <<< ДОБАВЛЕНО
        maxBytes=5_000_000,            # <<< ДОБАВЛЕНО (5 MB)
        backupCount=3                  # <<< ДОБАВЛЕНО
    )
    fh.setLevel(logging.WARNING)       # <<< ДОБАВЛЕНО
    fh.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
    ))                                 # <<< ДОБАВЛЕНО

    # Добавляем обработчики, если их ещё нет
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)          # <<< ДОБАВЛЕНО

    return logger
