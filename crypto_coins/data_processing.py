
import logging
from django.db import connection
import requests
from .okx_request import okx_request
from .models import CoinPrice, Token  


def data_processing():

    """Функция получает данные """

    tokens = Token.objects.all()  
    data = okx_request()
    if data:
        if "data" not in data:
            print(f"Ошибка API: {data}")
        else:
            conteiner = []
            for token in tokens:
                for ticker in data["data"]:
                    if ticker["instId"] == f"{token.symbol}-USDT":
                        conteiner.append(CoinPrice(price=float(ticker['last']), token=token))
                        print(f"✅ {ticker['instId']}: ${ticker['last']}")
            return conteiner