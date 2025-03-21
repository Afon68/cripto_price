import os
import time
import logging
from django.db import connection
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.utils.timezone import now
from crypto_coins.models import CoinPrice, Token  # Подставь свой путь
from selenium.common.exceptions import WebDriverException

import undetected_chromedriver as uc


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_prices(driver):
    """Функция получает цены всех токенов и записывает в БД"""
    tokens = Token.objects.only("symbol", "url_token")  # Загружаем только нужные поля
    for token in tokens:
        driver.get(token.url_token)  # Переход на сайт токена
        WebDriverWait(driver, 10).until(lambda d: " | " in d.execute_script("return document.title"))  
        title = driver.execute_script("return document.title")
        price = float(title.split("|")[0].strip().replace(",", ""))
        # Запись в БД
        CoinPrice.objects.create(price=price, token=token)
        logging.info(f"✅ Записали в БД: {token.symbol} = {price}")
    
    delete_entrys(tokens)
    get_table_size()

def get_table_size():
    with connection.cursor() as cursor:  # размер таблицы coinprice
        cursor.execute("SELECT pg_size_pretty(pg_total_relation_size('crypto_coins_coinprice'));")
        size = cursor.fetchone()
        print(size[0])  # объем таблицы CoinPrice в килобайтах




def start_selenium():
    """Запуск браузера через undetected_chromedriver"""
    for attempt in range(3):
        try:
            logging.info(f"🚀 Запуск undetected_chromedriver (попытка {attempt + 1}/3)")
            driver = uc.Chrome(headless=True, use_subprocess=False)
            logging.info("✅ Selenium успешно запущен!")
            return driver
        except Exception as e:
            logging.error(f"❌ Ошибка Selenium: {e},следующий запуск через 5 сек")
            time.sleep(5)

    logging.critical("⛔ Selenium не запустился после 3 попыток. Останавливаем работу.")
    return None

def price_token_from_rialto():
    """Бесконечный цикл сбора данных с автоматическим перезапуском браузера"""

    driver = start_selenium()  # 🚀 Первый запуск браузера 

    if driver is None:
        logging.critical("❌ Не удалось запустить Selenium! Выход из программы.")
        return  # 🚨 Прекращаем выполнение, если браузер не запустился

    t = 25  # Интервал между запросами
    while True:  # 🔄 Работает пока сервер не выключится
        try:
            logging.info("🔄 Обновляем цены...")
            fetch_prices(driver)  # 🔥 Функция парсинга
            logging.info(f"⏰ Следующее обновление через {t} секунд...")
            time.sleep(t)  # Ждём t секунд

        except WebDriverException as e:
            logging.warning(f"⚠ WebDriverException: {e}")
            logging.info("🔄 Перезапускаем браузер...")
            driver.quit()  # Закрываем текущий браузер
            driver = start_selenium()  # 🚀 Запускаем новый браузер NewConnectionError

            if driver is None:
                logging.critical("❌ Selenium не запустился после сбоя! Выход из цикла.")
                break  # 🚨 Прерываем while True, если браузер не восстановился
        
        except KeyboardInterrupt:
            logging.warning("⛔ Остановлено пользователем!")
            break  # 🚨 Выход из бесконечного цикла

        except Exception as e:
            logging.error(f"❌ Критическая ошибка: {e}")
            logging.info("🔄 Повторная попытка через 30 секунд...")
            time.sleep(30)  # Ждём перед повторным запуском
            driver.quit()  # Закрываем текущий браузер
            driver = start_selenium()  # 🚀 Запускаем новый брауз
    driver.quit()  # 🚪 Закрываем браузер при выходе
    logging.info("🚪 Браузер закрыт")

def delete_entrys(tokens):
    all_entrys = CoinPrice.objects.all()
    if len(all_entrys) > 1450 * len(tokens):
        dif_entrys = len(all_entrys) - 1450 * len(tokens)  # - кол-во записей для удаления 
        last_few = all_entrys.order_by('id')[:dif_entrys]  # Получаем последние 10 записей
        CoinPrice.objects.filter(id__in=last_few.values_list('id', flat=True)).delete()  # Удаляем их
        logging.info(f"🗑🧺 Удалены {dif_entrys} последние записи в БД")
        logging.info(f"🧮 Кол-во записей в CoinPrice = {len(all_entrys) - dif_entrys}")