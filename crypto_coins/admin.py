from django.contrib import admin
from crypto_coins.models import CoinPrice, Token



admin.site.register(Token)
admin.site.register(CoinPrice)

