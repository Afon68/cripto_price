import logging
import threading
import time
import psutil
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from .services import price_token_from_rialto
from .services import start_selenium  # Импортируем запуск Selenium

def check_memory():
    """Проверка свободной памяти и перезапуск Selenium при нехватке ОЗУ"""
    while True:
        mem = psutil.virtual_memory()
        if mem.available < 100 * 1024 * 1024:  # Если < 100MB свободно
            logging.warning(f"⚠ ОЗУ заканчивается!Осталось {mem.available} Перезапускаем Selenium...")
            start_selenium()  # Перезапускаем Selenium
        time.sleep(10)  # Проверяем каждые 10 секунд

def start():
    """Запуск фоновых процессов при старте Django"""
    print("✅ Запускаем Selenium при старте Django...")
    
    # Запускаем `price_token_from_rialto` в фоне
    threading.Thread(target=price_token_from_rialto, daemon=True).start()
    
    # 🔥 Добавляем поток для контроля памяти
    threading.Thread(target=check_memory, daemon=True).start()
    
    # Если нужны другие фоновые задачи, оставляем планировщик
    scheduler = BackgroundScheduler()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown(wait=False))



   

