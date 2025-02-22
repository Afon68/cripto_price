from .services import price_token_from_rialto
from crypto_coins.models import CoinPrice, Token
from django.shortcuts import get_object_or_404



def write_to_db():
    prices = price_token_from_rialto()
    if prices:
        for i in prices:
            # token, _ = Token.objects.get_or_create(symbol=i)
            token = get_object_or_404(Token,symbol=i)
            last_price = CoinPrice.objects.filter(token__symbol=i).first()
            if last_price is None or float(last_price.price) != prices[i]:
                CoinPrice.objects.create(price=prices[i], token=token)
                print(f"✅Запись в БД сделана !:{token.name} = {prices[i]}🚀💪")
    else:
        print("❌ Данные с биржи не пришли - записывать нечего в БД")
        return
    
"""Использование get_or_create
token, _ = Token.objects.get_or_create(symbol=i)
⛔ Проблема: get_or_create создаст токен, если его нет, но если он уже есть, то новый не обновится!
✅ Решение: Использовать update_or_create()

python
Копировать
Редактировать
token, _ = Token.objects.update_or_create(symbol=i, defaults={"name": i})"""

