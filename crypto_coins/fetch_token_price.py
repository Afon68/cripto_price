import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crypto_coins.models import Token, CoinPrice  # Импорт моделей

# Настройка Selenium (один раз для всех потоков)
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Асинхронная функция для получения цены токена
def fetch_token_price(token):
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(token.url_token)
        
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.title") and " | " in d.execute_script("return document.title")
        )
        title = driver.execute_script("return document.title;")
        price = float(title.split("|")[0].strip().replace(',', ''))
        
        CoinPrice.objects.create(price=price, token=token)
        print(f"🔥 Запись в БД: {token.name} = {price} 🚀")

    except Exception as e:
        print(f"❌ Ошибка для {token.name}: {e}")
    finally:
        driver.quit()

# Асинхронный запуск всех задач сразу
async def run_all_tokens():
    tokens = Token.objects.all()
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await asyncio.gather(*[loop.run_in_executor(pool, fetch_token_price, token) for token in tokens])

# Запуск
asyncio.run(run_all_tokens())
