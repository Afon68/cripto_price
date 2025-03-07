import logging
from django.shortcuts import get_object_or_404
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import selenium

from crypto_coins.models import CoinPrice 
from crypto_coins.models import Token
from django.db import connection


print(f"selenium.__version__ = {selenium.__version__}")
# from selenium.webdriver.chrome.service import  WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeDriverManager
import webdriver_manager

"""Настройка логирования
Это стандартный формат логирования, который автоматически подставляет:

%(asctime)s → текущее время
%(levelname)s → уровень логирования (INFO, ERROR и т. д.)
%(message)s → само сообщение"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def price_token_from_rialto():
    """Функция сбора данных о цене токенов и записи в БД."""
    # Настройка Selenium
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")  # Без графического интерфейса
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"❌ Ошибка запуска Selenium: {e}")
        return None
    
    prices = []
    tokens = Token.objects.all()
    if tokens:
        for item in tokens:

          
            driver.get(item.url_token)

            # Ждём появления тэга
            # try:
            #     WebDriverWait(driver, 15).until(
            #         EC.presence_of_element_located((By.TAG_NAME, "title"))
            #     )
            #     print("✅ Тэг найден!")
            # except:
            #     print("❌ Тэг не появился, возможно, данные подгружаются позже!")
        
            # print("🔥Ура !!!!!! Информацию получил !!!!!!! Обрабатываю !!!!!💪🚀")
            # 🔥 Даем странице прогрузиться
        
            
            try:
                # print("В цикле")
                # time.sleep(5)
                # Делаем скриншот
                # driver.get_screenshot_as_file("screenshot.png")
                # Получаем HTML
                
                # time.sleep(5)
                # title = driver.find_element(By.TAG_NAME, "title").text
                
                # html = driver.page_source
                # soup = BeautifulSoup(html, "html.parser")

                # Находим таблицы
                # title = soup.find_all("title")
                # print(title)
                # eth_price = float(title[0].text.split("|")[0].strip().replace(',', ''))
                # price = float(title[0].text.split("|")[0].strip().replace(',', ''))
                # print(price)
#                 Что делает этот код?

                # Ждет, пока document.title загрузится и в нем появится " | " (разделитель цен).
                # Извлекает title через execute_script, без find_element().
                # Парсит цену, убирая запятые.
                # title = driver.execute_script("return document.title;")
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.title") and " | " in d.execute_script("return document.title")
                )
                title = driver.execute_script("return document.title;")  # Этот код берет заголовок напрямую из DOM с помощью JavaScript.
                # print(f"✅ title = {title}")
                price = float(title.split("|")[0].strip().replace(',', ''))
                # print(f"✅ Цена {item.symbol} = {price}")
                # token, _ = Token.objects.get_or_create(name="Ethereum")
                # token = get_object_or_404(Token,name=item.name)
                # print(f'✅ token = {token}')
                # print(item.symbol)
                # (ETH) Bitcoin (BTC)
                if price:
                    prices.append(CoinPrice(price=price, token=item))
                    logging.info(f"🔥Запись в список prices сделана !🚀💪:Цена {item.name} = {price}")
                    delete_entrys()
                    
                else:
                    print("❌ Данные от поставщика не пришли - записывать нечего в БД")
                    return
                # prices[item.symbol] = price
                
            except Exception as e:
                print("❌ Тэг не появился, возможно, данные подгружаются позже!")
                continue  # Продолжаем выполнение для других токенов
    else:
        print("❌ Нет связи с БД")
        return None 
    CoinPrice.objects.bulk_create(prices)
    logging.info(f"🔥Запись в БД  списка через bulk_create(prices) сделана !🚀💪")
    logging.info(f"✅ Объём БД должна быть не более {1450 * len(tokens)} записей")
        # # Закрываем браузер
    driver.quit()
    logging.info("✅ Следующая запись в БД через 1 минуту")
    # delete_entrys()
    logging.info(f"✅Кол-во записей в CoinPrice = {len(CoinPrice.objects.all())}")
    with connection.cursor() as cursor: # размер таблицы coinprice
        cursor.execute("SELECT pg_size_pretty(pg_total_relation_size('crypto_coins_coinprice'));")
        size = cursor.fetchone()
        print(f"size = {size[0]}")
    return True


def delete_entrys():
    # logging.info(f"✅Кол-во записей в CoinPrice = {len(CoinPrice.objects.all())}")
    if len(CoinPrice.objects.all()) > 1450 * len(tokens):
        CoinPrice.objects.last().delete()
   
        # CoinPrice.objects.filter(id__lt=4).delete()
    # print(prices)
    # return prices

    # return tariffs
    # # 🔥 Настройки Selenium
    # service = Service(ChromeDriverManager().install())
    # options = Options()
    # options.add_argument("--headless")  # Без интерфейса
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")

    # driver = webdriver.Chrome(service=service, options=options)
    # driver.get("https://example.com")  # Заменить на реальный сайт

    # time.sleep(5)  # Даем странице прогрузиться
    
    # # ✅ Считываем данные
    # html = driver.page_source
    # soup = BeautifulSoup(html, "html.parser")
    
    # price_element = soup.find("div", class_="price").text.strip().replace(",", ".")
    # price = float(price_element)

    # # ✅ Находим токен (Ethereum)
    # token, _ = Tokens.objects.get_or_create(name="Ethereum")

    # # ✅ Записываем цену в БД
    # CoinPrice.objects.create(price=price, token=token)
    # print(f"✅ Записали в БД: {token.name} = {price} USD")
    # CoinPrice.objects.filter(token__symbol="BTC").order_by('-timestamp').first()
    # driver.quit()
