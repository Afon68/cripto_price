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


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_prices(driver):
    """Функция получает цены всех токенов и записывает в БД"""
    tokens = Token.objects.only("symbol", "url_token")  # Загружаем только нужные поля
    
    for token in tokens:
        # try:
            driver.get(token.url_token)  # Переход на сайт токена
            WebDriverWait(driver, 10).until(lambda d: " | " in d.execute_script("return document.title"))  
            title = driver.execute_script("return document.title")
            price = float(title.split("|")[0].strip().replace(",", ""))
            
            # Запись в БД
            CoinPrice.objects.create(price=price, token=token)
            logging.info(f"✅ Записали в БД: {token.symbol} = {price}")

        # except WebDriverException as e:
        #     logging.warning(f"❌Ошибка ⚠ WebDriverException: {e}")
        #     logging.info("🔄 браузер Перезапускаем ...")
        #     driver.quit()  # Закрываем текущий браузер
        #     driver = start_selenium()  # 🚀 Запускаем новый браузер    
            
        # except Exception as e:
        #     logging.error(f"❌ Цикл for Ошибка получения цены {token.symbol}: {e}")
        #     logging.info(f"✅ Закрываем браузер")
        #     driver.quit()
            # return
            # logging.info(f"✅ Открываем браузер снова")
            # driver = start_selenium()  # 🚀 Первый запуск браузера 

            # if driver is None:
            #     logging.critical("❌ Не удалось запустить Selenium! Выход из программы.")
            #     return  # 🚨 Прекращаем выполнение, если браузер не запустился

    delete_entrys(tokens)
    with connection.cursor() as cursor: # размер таблицы coinprice
        cursor.execute("SELECT pg_size_pretty(pg_total_relation_size('crypto_coins_coinprice'));")
        size = cursor.fetchone()
        print(f"size = {size[0]}")

# def price_token_from_rialto():
#     """Основной цикл: Запускает Selenium и обновляет цены бесконечно"""
#     while True:
#         try:
#             logging.info("🚀 Запускаем Selenium...")

#             # Создаем **один** браузер на весь процесс
#             service = Service(ChromeDriverManager().install())
#             options = Options()
#             options.add_argument("--headless")  # Без графического интерфейса (можно убрать для тестов)
#             options.add_argument("--disable-gpu")
#             options.add_argument("--no-sandbox")
            
#             driver = webdriver.Chrome(service=service, options=options)
#             t = 20
#             try:
#                 while True:
#                     logging.info("🔄 Обновляем цены...")
#                     fetch_prices(driver)  # Собираем данные
                    
#                     logging.info(f"⏳ Ожидание {t} сек перед следующей итерацией...")
#                     time.sleep(t)  # Ждём t cекунд
#             except WebDriverException as e:
#                             print(f"⚠ WebDriverException: {e}")
#                             print("🔄 Перезапускаем браузер...")
#                             break  # Выходим из вложенного цикла, чтобы перезапустить браузер
#             except KeyboardInterrupt:
#                 logging.warning("⛔ Остановлено пользователем!")
#             except Exception as e:
#                 logging.error(f"❌ Критическая ошибка: {e}")
#             finally:
#                 driver.quit()  # Закрываем браузер
#                 logging.info("🚪 Браузер закрыт")

#         except Exception as e:
#             print(f"❌ Ошибка: {e}")
#             print("🔄 Повторная попытка через 30 секунд...")
#             time.sleep(30)  # Ждём перед повторным запуском
# # ✅ Запускаем бесконечный цикл

# ///<<!!!!!!! Все тоже сомое, что и код выше, только без большого while и break - интересно!!!!!

def start_selenium():

    """Запускает и возвращает экземпляр браузера Chrome"""
    
    try:
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")  # Без графического интерфейса
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        return webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        logging.error(f"❌ Ошибка запуска Selenium: {e}")
        return None  # 🚨 Если Selenium не запустился, возвращаем None

def price_token_from_rialto():
    """Бесконечный цикл сбора данных с автоматическим перезапуском браузера"""

    driver = start_selenium()  # 🚀 Первый запуск браузера 

    if driver is None:
        logging.critical("❌ Не удалось запустить Selenium! Выход из программы.")
        return  # 🚨 Прекращаем выполнение, если браузер не запустился

    t = 40  # Интервал между запросами
    while True:  # 🔄 Работает пока сервер не выключится
        try:
            logging.info("🔄 Обновляем цены...")
            fetch_prices(driver)  # 🔥 Функция парсинга
            logging.info(f"⏳ Следующее обновление через {t} секунд...")
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

        
        # finally:
        #     driver.quit()  # Закрываем браузер
        #     logging.info("🚪 Браузер закрыт")



def delete_entrys(tokens):
    all_entrys = CoinPrice.objects.all()
    logging.info(f"✅Кол-во записей в CoinPrice = {len(all_entrys)}")
    if len(all_entrys) > 1450 * len(tokens):
        dif_entrys = len(all_entrys) - 1450 * len(tokens)  # - кол-во записей для удаления 
        last_few = all_entrys.order_by('id')[:dif_entrys]  # Получаем последние 10 записей
        CoinPrice.objects.filter(id__in=last_few.values_list('id', flat=True)).delete()  # Удаляем их
        # x =CoinPrice.objects.last().delete()
        logging.info(f"❌ Удалены {dif_entrys} последние записи в БД")
        logging.info(f"✅Кол-во записей в CoinPrice = {len(all_entrys) - dif_entrys}")