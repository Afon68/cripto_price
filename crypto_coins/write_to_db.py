import logging
from django.db import connection
from .data_processing import data_processing
from .models import CoinPrice
from django.utils.timezone import  now, timedelta



def write_to_db():
    
    prices = data_processing()
    if prices:
        CoinPrice.objects.bulk_create(prices)
        print(f"✅ {len(prices)} объектов записано в CoinPrice ") 
    else:
        print("❌ Данные с биржи не пришли - записывать нечего в БД")
        return
    
    delete_entrys(prices)
    connect()


def delete_entrys(tokens):

    all_entrys = CoinPrice.objects.all()
    print(f"{now()}🧮 Кол-во записей в CoinPrice = {len(all_entrys)}")

    if len(all_entrys) > 1450 * len(tokens):
        dif_entrys = len(all_entrys) - 1450 * len(tokens)  # - кол-во записей для удаления 
        last_few = all_entrys.order_by('id')[:dif_entrys]  # Получаем последние {dif_entrys} записей превышающие лимит
        CoinPrice.objects.filter(id__in=last_few.values_list('id', flat=True)).delete()  # Удаляем их
        print(f"{now()}🗑🧺 Удалены {dif_entrys} последние записи в БД")
        print(f"{now()}🧮 Кол-во записей в CoinPrice = {len(all_entrys) - dif_entrys}")


def connect():
    with connection.cursor() as cursor: # размер таблицы coinprice
            cursor.execute("SELECT pg_size_pretty(pg_total_relation_size('crypto_coins_coinprice'));")
            size = cursor.fetchone()
            print(f"База данных весит {size[0]}")
        

