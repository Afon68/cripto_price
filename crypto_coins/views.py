import datetime
import logging
from django.db.models import F
from django.shortcuts import render
from django.template import context


from .models import CoinPrice, Token
from django.utils.timezone import localtime, now, timedelta
from datetime import timedelta, datetime
from django.http import JsonResponse
from .utils import round_number
import threading
from .services import price_token_from_rialto
from .utils import start_selenium_if_needed


def get_latest_price_list(request,token_symbol,time_frame,period):    # ,time_frame
    tokens = Token.objects.all()
    last_all_price = []
    for token in tokens:
        latest_prices = CoinPrice.objects.filter(token=token).order_by('-timestamp')[:2]
    
        if latest_prices:
            dif = round(latest_prices[0].price - latest_prices[1].price, 2)
            last_all_price.append({"price": round_number(latest_prices[0].price), "dif": dif , "name":latest_prices[0].token.name})
        else:
            "❌ Ошибка: latest_prices не найден!"
    
    # if latest_prices:
    #     dif_time = now() - latest_prices[0].timestamp
    #     print(f"🔍 Проверка в views времени последней записи : {dif_time},{latest_prices[0].token.name}")
    #     if dif_time > timedelta(minutes=5):  # Если данных нет 5+ минут
    #         start_selenium_if_needed(latest_prices)
    # Текущий момент времени
    current_time = now()
    token = Token.objects.get(symbol=token_symbol)
    # latest_prices = CoinPrice.objects.order_by('-timestamp')[:len(tokens) * 2]
    # Фильтруем записи за последние 24 часа через каждый час
    # last_all_price = [{"name":p.token.name,"price": round_number(p.price)} for p in latest_prices]
    
    hourly_prices = CoinPrice.objects.filter(token=token,timestamp__gte=current_time - timedelta(hours=period)  # За последние 24 часа  days
                                                                    ).annotate(
                                                                        hour=F('timestamp__minute')  # Добавляем поле "час"  hour
                                                                        ).order_by('-timestamp','hour')  # 🔥 Сначала сортируем по "hour"
    v_db = len(CoinPrice.objects.filter(token__symbol=token_symbol))
    
    print(f"Объем БД CoinPrice = {len(CoinPrice.objects.all())}")
    print(f"Объем БД CoinPrice токену {token.name} = {v_db}")
    print(f"Длина списка по {token.name}  = {len(hourly_prices)}")
    # 🔥 Берём только первую запись для каждого часа
    # unique_hours = {}
    # time_frame = 30
    
            
    # for price in hourly_prices:
    #     # if price.hour not in unique_hours:  
    #     if price.hour % time_frame == 0 or price.hour % time_frame == 14 or price.hour % time_frame == 1 :  
    #         # unique_hours[price.hour] = True  # Запоминаем час
    #         last_price.append(price)  # Добавляем в результат
    # for i in range(len(hourly_prices)):
    #     if i > 0 and i < len(hourly_prices) - 1:
    #         if hourly_prices[i].hour % time_frame == 0:
    #             last_price.append(hourly_prices[i])
    #         elif hourly_prices[i].hour % time_frame != 0 and hourly_prices[i-1].hour % time_frame == 1:
    #             last_price.append(hourly_prices[i-1])
    #         elif hourly_prices[i].hour % time_frame != 0 and hourly_prices[i+1].hour % time_frame == time_frame - 1:
    #             last_price.append(hourly_prices[i+1])
    #         # elif hourly_prices[i].hour % time_frame != 0 and hourly_prices[i+1].hour % time_frame != 14 and hourly_prices[i-1].hour % time_frame == 1:
            #     last_price.append(hourly_prices[i-1])
    # i = 0            
    # while i < len(hourly_prices):
    #     if i > 0 and i < len(hourly_prices) - 1:
    #         if hourly_prices[i].hour % time_frame == 0:
    #             last_price.append(hourly_prices[i])
    #         elif hourly_prices[i].hour % time_frame != 0 and hourly_prices[i-1].hour % time_frame == 1:
    #             last_price.append(hourly_prices[i-1])
    #             i += 1
    #         elif hourly_prices[i].hour % time_frame != 0 and hourly_prices[i+1].hour % time_frame == time_frame - 1:
    #             last_price.append(hourly_prices[i+1])
    #             i += 1
    #     i += 1    
            
            
    # if hourly_prices[len(hourly_prices) - 1].hour % time_frame == 0:
    #     last_price.append(hourly_prices[len(hourly_prices) - 1])
    last_price = []
    logging.info(f"time_frame = {time_frame}") 
    if hourly_prices:
        last_price.append(hourly_prices[0])
        i = 1            
        while i < len(hourly_prices):
            if i > 1 and i < len(hourly_prices) - 1:
                if hourly_prices[i].hour != hourly_prices[i+1].hour:
                    # i += 1
                    # continue
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


    # logging.info(f"unique_hours= {unique_hours}")
    logging.info(f"last_price = {len(last_price)}")
    logging.info(f"last_price = {last_price}")

    # last_price = CoinPrice.objects.filter(token__symbol=token_symbol)[:25] # Последние 24 записи

    prices_with_diff = []
    if last_price:
        for i in range(len(last_price)):
            last_price[i].timestamp = localtime(last_price[i].timestamp).strftime("%d.%m.%Y %H:%M:%S")
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
    # logging.info(f"prices_with_diff = {prices_with_diff}")
    print("✅ Отправляем данные с views.get_latest_price_list на фронт(update_list.js.then(response => response.json()))")
    return JsonResponse({"price_list": prices_with_diff if prices_with_diff else "Нет списка данных prices_with_diff",
                         "last_all_price": last_all_price if last_all_price else "Нет списка данных last_all_price"})


def token_price_with_js_view(request):
    time_frames = [["1 min","1"],["5 min","5"],["15 min","15"],["30 min","30"],["1 hour","60"]]
    time_periods = {"1 hour":"1", "12 hour":"12", "24 hour": "24"}
    periods = time_periods.items()
    url_icon = ["crypto_coins/images/ETH.png", "crypto_coins/images/BTC.png", "crypto_coins/images/SOL.png", "crypto_coins/images/STRK.png"] 
    coins = Token.objects.all()
    tokens = []
    for i in range(len(coins)):
        tokens.append({"name": coins[i].name, "symbol": coins[i].symbol, "url_icon": url_icon[i]})
    context = {
        "tokens": tokens,
        "time_frames": time_frames,
        "time_periods": periods,
    }
    return render(request, "token_price.html", context)


