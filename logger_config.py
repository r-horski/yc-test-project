import logging
from config import LOG_FILE

def setup_logger():
    logger = logging.getLogger("OrderProcessor")
    logger.setLevel(logging.INFO)

    # Избегаем дублирования обработчиков
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Файл
        fh = logging.FileHandler(LOG_FILE)
        fh.setFormatter(formatter)

        # Консоль
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger