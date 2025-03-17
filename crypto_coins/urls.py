from django.urls import path
# from .views import eth_price_view
# from .views import get_latest_price
from .views import get_latest_price_list
from .views import token_price_with_js_view
from .views import hello_view



app_name = 'crypto_coins'

urlpatterns = [
    path('', hello_view, name="hello"),
    path('cripta/', token_price_with_js_view, name="token_price"),
    path('latest-price-list/<str:token_symbol>/<int:time_frame>/<int:period>/', get_latest_price_list, name="latest_price-list"),      # <int:time_frame>/
]



# urlpatterns = [
#     path("", eth_price_with_js_view, name="eth_price"),
#     path("play/", playing_view, name="playing"),
#     path('latest-price/', get_latest_price, name="latest_price"),  # ✅ API для цены
#     # ✅ Теперь по адресу http://127.0.0.1:8000/latest-price/ будет JSON с ценой.
#     path('latest-price-list/', get_latest_price_list, name="latest_price-list"),  # ✅ API для цены

# ]