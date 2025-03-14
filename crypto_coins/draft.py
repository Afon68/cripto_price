from crypto_coins.models import CoinPrice, Token
from django.utils.timezone import localtime, now, timedelta
from datetime import timedelta, datetime

import symbol


# for i in range(61):
#     if (i + 23) % 15 == 0:
#         print(i)




y = []
x = [1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 9]
for i in range(len(x)):
    if i < len(x) - 1:
        if x[i] == x[i + 1]:
            continue
        if x[i] % 1 == 0:
            y.append(x[i]) 
print(y)      


def price_change_percentage(back_price, now_price):
    
    # функция  для для вычисления изменения числа в %

    # x = 80  # какое число было
    # y = 76.6  # какое число стало
    z = 100 - 100 * now_price / back_price if back_price > now_price else -(100 - 100 * now_price / back_price)  # изменение в %
    dif = "упал" if back_price > now_price else "вырос"

    print(f"{back_price} {dif} на {round(z, 2)}% и стало {now_price}")
    print(f"часть в % = {100 * now_price / back_price}") 

price_change_percentage(80, 120)                                                                