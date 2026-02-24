# database.py
import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger("OrderProcessor")

class OrderDatabase:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """Создаёт таблицу, если не существует"""
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id TEXT PRIMARY KEY,
                        status TEXT,
                        date TEXT,
                        amount REAL,
                        customer_region TEXT,
                        inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            logger.info("✅ Таблица 'orders' готова к работе.")
        except Exception as e:
            logger.critical(f"❌ Ошибка при инициализации БД: {e}")
            raise

    def insert_order(self, order):
        """Вставляет заказ, если его ещё нет"""
        query_check = "SELECT 1 FROM orders WHERE order_id = ?"
        query_insert = """
            INSERT INTO orders (order_id, status, date, amount, customer_region)
            VALUES (?, ?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(query_check, (order["order_id"],))
                if cursor.fetchone() is None:
                    cursor.execute(query_insert, (
                        order["order_id"],
                        order["status"],
                        order["date"].replace('T', ' '),
                        order["amount"],
                        order["customer"]["region"]
                    ))
                    logger.info(f" Добавлен заказ: {order['order_id']}")
                    return True
                else:
                    logger.debug(f" Пропущен дубликат: {order['order_id']}")
                    return False
        except Exception as e:
            logger.error(f" Ошибка при вставке заказа {order['order_id']}: {e}")
            return False