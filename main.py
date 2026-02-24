import json
import sqlite3
import logging
from datetime import datetime
import os

# Настройка логирования (после создания папки)

DB_PATH = "db/orders.db"
JSON_PATH = "orders.json"


def setup_logging():
    """"Настраивает логирование после создания папки logs"""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/process.log"),
            logging.StreamHandler()
        ]
    )


def create_db():
    """Создаёт таблицу orders, если не существует"""
    if not os.path.exists("db"):
        os.makedirs("db")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            status TEXT,
            date TEXT,
            amount REAL,
            customer_region TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Таблица orders создана или уже существует.")


def load_json_data():
    """Читает данные из JSON-файла"""
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Загружено {len(data)} заказов из {JSON_PATH}")
        return data
    except Exception as e:
        logging.error(f"Ошибка при чтении JSON: {e}")
        return []


def insert_orders(data):
    """Вставляет заказы, избегая дубликатов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted = 0
    for order in data:
        order_id = order["order_id"]
        status = order["status"]
        # Преобразуем ISO-формат в 'YYYY-MM-DD HH:MM:SS'
        date_str = order["date"].replace('T', ' ')
        amount = order["amount"]
        customer_region = order["customer"]["region"]

        # Проверка на дубликат
        cursor.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,))
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO orders (order_id, status, date, amount, customer_region)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, status, date_str, amount, customer_region))
            inserted += 1
        else:
            logging.info(f"Пропущен дубликат: {order_id}")

    conn.commit()
    conn.close()
    logging.info(f"Успешно добавлено {inserted} новых заказов.")


def main():
    logging.info("Запуск процесса загрузки данных.")

    # Создаём директории, если их нет
    for directory in ["logs", "db"]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Создана директория: {directory}")

    setup_logging()  # Теперь логирование настраивается после создания папки
    
    create_db()
    data = load_json_data()
    if data:
        insert_orders(data)
    else:
        logging.error("Нет данных для вставки.")

    logging.info("Процесс завершён.")

if __name__ == "__main__":
    # Инициализируем логирование вручную сначала
    logging.basicConfig(level=logging.INFO)
    main()