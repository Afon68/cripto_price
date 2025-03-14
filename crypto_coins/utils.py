import threading
from datetime import timedelta
from django.utils.timezone import now
from .models import CoinPrice
from .services import price_token_from_rialto  # Импортируем сам парсер


def round_number(number):
    if not number:
        return False
    elif number < 0:
        return round(number, 2)
    elif number < 0.001:
        return round(number, 6)
    elif number < 0.01:
        return round(number, 6)
    elif number < 0.1:
        return round(number, 5)
    elif number < 1:
        return round(number, 4)
    elif number < 10:
        return round(number, 3)
    elif number >= 10:
        return round(number, 2)
    
from django.db import connection

def get_table_size():
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_size_pretty(pg_total_relation_size('crypto_coins_coinprice'));")
        size = cursor.fetchone()
        print(size[0])

print(get_table_size())  # Выведет размер таблицы, например, '10 MB'


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Глобальный флаг для проверки, работает ли уже Selenium
last_fetch_thread = None  

def start_selenium_if_needed(latest_prices):
    """Запускает Selenium, если данные устарели."""
    global last_fetch_thread

    if latest_prices:
        dif_time = now() - latest_prices[0].timestamp
        print(f"🔍 Проверка в utils времени последней записи: {dif_time},{latest_prices[0].token.name}")
        if dif_time > timedelta(minutes=5):  # Если данных нет 5+ минут
            if last_fetch_thread is None or not last_fetch_thread.is_alive():
                print("🚀 Запускаем Selenium в фоне...")
                last_fetch_thread = threading.Thread(target=price_token_from_rialto, daemon=True)
                last_fetch_thread.start()
            else:
                print("⚠ Selenium уже работает, новый запуск не нужен.")
    else:
        print("⚠ В базе нет данных, запускаем Selenium...")
        last_fetch_thread = threading.Thread(target=price_token_from_rialto, daemon=True)
        last_fetch_thread.start()

def price_change_percentage(back_price, now_price):
    # функция  для для вычисления изменения числа в %
    z = round(100 - 100 * now_price / back_price, 2)      
    
    return z

   
