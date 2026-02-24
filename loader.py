import json
import logging
from config import JSON_PATH

logger = logging.getLogger("OrderProcessor")

def load_orders():
    """Загружает заказы из JSON-файла"""
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f" Загружено {len(data)} заказов из {JSON_PATH}")
        return data
    except FileNotFoundError:
        logger.critical(f" Файл не найден: {JSON_PATH}. Убедитесь, что он находится в папке 'data/'.")
        return []
    except json.JSONDecodeError as e:
        logger.critical(f" Ошибка парсинга JSON: {e}")
        return []
    except Exception as e:
        logger.critical(f" Непредвиденная ошибка при чтении файла: {e}")
        return []