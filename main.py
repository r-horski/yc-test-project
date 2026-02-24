# main.py
import argparse
from config import JSON_PATH
from database import OrderDatabase
from loader import load_orders
from logger_config import setup_logger

def show_stats():
    """Показывает статистику по базе"""
    import sqlite3
    from config import DB_PATH

    with sqlite3.connect(DB_PATH) as conn:
        count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        total_amount = conn.execute("SELECT SUM(amount) FROM orders").fetchone()[0]
        latest = conn.execute("SELECT MAX(date) FROM orders").fetchone()[0]

    print(f"\n Статистика:")
    print(f"   Всего заказов: {count}")
    print(f"   Общая сумма: {total_amount or 0:.2f} ₽")
    print(f"   Последний заказ: {latest}")

def main():
    parser = argparse.ArgumentParser(description="Загрузка заказов в SQLite")
    parser.add_argument("--stats", action="store_true", help="Показать статистику после загрузки")
    args = parser.parse_args()

    logger = setup_logger()
    logger.info("🚀 Запуск обработки заказов...")

    # Проверка наличия файла
    if not os.path.exists(JSON_PATH):
        logger.critical(f"Файл данных не найден: {JSON_PATH}")
        return

    # Инициализация
    db = OrderDatabase()
    orders = load_orders()

    if not orders:
        logger.critical(" Нет данных для обработки. Завершение.")
        return

    # Загрузка
    inserted = 0
    for order in orders:
        if db.insert_order(order):
            inserted += 1

    logger.info(f" Загрузка завершена: добавлено {inserted} новых заказов.")

    if args.stats:
        show_stats()

if __name__ == "__main__":
    import os  # нужно для main
    main()