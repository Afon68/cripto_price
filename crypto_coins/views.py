import datetime
import logging
from django.db.models import F
from django.shortcuts import render
from django.template import context
from django.templatetags import static
from urllib3 import request

from cripto_currency.settings import DEBUG


from .models import CoinPrice, Token
from django.utils.timezone import localtime, now, timedelta
from datetime import timedelta, datetime
from django.http import JsonResponse
from .utils import round_number
import threading
from .services import price_token_from_rialto




def for_running_line(request,period):    # ,time_frame
    tokens = Token.objects.all()
    last_all_price = []
    for token in tokens:
        latest_prices = CoinPrice.objects.filter(token=token).order_by('-timestamp')[:2]
        back_period_hours = CoinPrice.objects.filter(token=token,timestamp__gte=now() - timedelta(hours=period)).order_by('timestamp')[1]
        url_icon = f"https://bin.bnbstatic.com/static/assets/logos/{token.symbol}.png"
        # url_icon = f"http://127.0.0.1:8000/static/crypto_coins/images/{token.symbol}.png" # 👈 Генерируем полный URL
        print(f"url_icon = {url_icon}")
         
        if latest_prices:
            if back_period_hours:
                # изменения цены в %
                price_change_percentage= (round(100 - 100 * latest_prices[0].price / back_period_hours.price, 2)) * (-1)
                print(f"✅ back_period_hours = {back_period_hours.price}")
                dif = round_number(latest_prices[0].price) - round_number(latest_prices[1].price)
                last_all_price.append({"price": round_number(latest_prices[0].price), "dif": dif , "name":latest_prices[0].token.name,
                                        "url_icon": url_icon,"price_change_percentage": price_change_percentage })
            else:
                dif = round(latest_prices[0].price - latest_prices[1].price, 2)
                last_all_price.append({"price": round_number(latest_prices[0].price), "dif": dif , "name":latest_prices[0].token.name,
                                            "url_icon": url_icon,"price_change_percentage": 0.00 })        
        else:
            "❌ Ошибка: объектов в latest_prices нет!"
      # За последние 24 часа  days
    print(f"back_period_hours = {back_period_hours}")
    return last_all_price
   

def get_latest_price_list(request,token_symbol,time_frame,period):
    # Текущий момент времени
    current_time = now()
    # выборка данных согласно токену и периоду и создается поле "hour" для отбора данных по тайм-фрейму
    hourly_prices = CoinPrice.objects.filter(token__symbol=token_symbol,timestamp__gte=current_time - timedelta(hours=period)  # За последние 24 часа  days
                                                                    ).annotate(
                                                                        hour=F('timestamp__minute')  # Добавляем поле "час"  minute
                                                                        ).order_by('-timestamp','hour')  # 🔥 Сначала сортируем по "timestamp"
    if hourly_prices:
        print(f"Кол-во записей в БД за {period} час(ов/а) по {hourly_prices[0].token.name}  = {len(hourly_prices)}")
    
    last_price = select_time_frame(hourly_prices,time_frame)

    prices_with_diff = data_for_table_chart(last_price)

    last_all_price = for_running_line(request,period)

    print("✅ Отправляем данные с views.get_latest_price_list на фронт(update_list.js.then(response => response.json()))")
    return JsonResponse({"price_list": prices_with_diff if prices_with_diff else "Нет списка данных prices_with_diff",
                         "last_all_price": last_all_price if last_all_price else "Нет списка данных last_all_price"})

# функция, котораая выбирает данные(объекты, экземпляры, записи) согласно тайм-фрейму
def select_time_frame(hourly_prices,time_frame):
    last_price = []
    logging.info(f"time_frame = {time_frame}") 
    if hourly_prices:
        last_price.append(hourly_prices[0])
        i = 0            
        while i < len(hourly_prices):
            if i > 0 and i < len(hourly_prices) - 1:
                if hourly_prices[i].hour != hourly_prices[i+1].hour:
                    if (hourly_prices[i].hour - hourly_prices[0].hour) % time_frame == 0:
                        last_price.append(hourly_prices[i])
                    elif (hourly_prices[i].hour - hourly_prices[0].hour) % time_frame != 0 and (hourly_prices[i-1].hour - hourly_prices[0].hour) % time_frame == 1:
                        last_price.append(hourly_prices[i-1])
                        i += 1
                    elif (hourly_prices[i].hour - hourly_prices[0].hour) % time_frame != 0 and (hourly_prices[i+1].hour - hourly_prices[0].hour) % time_frame == time_frame - 1:
                        last_price.append(hourly_prices[i+1])
                        i += 1
            i += 1    
    else:
        logging.info("❌ В БД нет запрашиваемых данных(наверное прошло более суток)")
    logging.info(f"last_price = {len(last_price)}")
    logging.info(f"last_price = {last_price}")

    return last_price 

# В этой функции формируется объект для отправки на фронт
def data_for_table_chart(last_price):
    prices_with_diff = []
    if last_price:
        for i in range(len(last_price)):
            if i != len(last_price) - 1:
                diff = round_number(last_price[i].price) - round_number(last_price[i+1].price)  # ✅ Вычитаем здесь
                if diff > 0:
                    direction = '<span class="up"> &uarr;</span>'  # 🔼 Красная стрелка вверх
                elif diff < 0:
                    direction = '<span class="down">&darr;</span>'  # 🔽 Зелёная стрелка вниз
                else:
                    direction = '<span class="up"> &uarr;</span>''<span class="down">&darr;</span>'  # ➖ Серый прочерк
            else:
                diff = None
                direction = '<span class="up"> &uarr;</span>''<span class="down">&darr;</span>'  # Если данных ещё нет
        
            prices_with_diff.append({"timestamp":last_price[i].timestamp,"price": round_number(last_price[i].price), "diff": diff, "direction": direction, "name":last_price[i].token.name, "hour": last_price[i].hour})
    else:
        logging.error("❌ Ошибка: в списке last_price нет данных") 

    return  prices_with_diff  
   
# Данные для html страницы
def token_price_with_js_view(request):
    time_frames = [["1 min","1"],["5 min","5"],["15 min","15"],["30 min","30"],["1 hour","60"]]
    time_periods = {"1 hour":"1", "12 hour":"12", "24 hour": "24"}
    periods = time_periods.items()
    coins = Token.objects.all()
    tokens = []
    for i in range(len(coins)):
        url_avatar = f"https://bin.bnbstatic.com/static/assets/logos/{coins[i].symbol}.png"
        tokens.append({"name": coins[i].name, "symbol": coins[i].symbol, "url_avatar": url_avatar})
    context = {
        "tokens": tokens,
        "time_frames": time_frames,
        "time_periods": periods,
    }
    return render(request, "token_price.html", context)


def hello_view(request):
    return render(request, "hello.html")