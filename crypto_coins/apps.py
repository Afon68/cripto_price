from django.apps import AppConfig
import os

# print("Этот принт стоит сразу после импорта в apps.py")
class CryptoCoinsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crypto_coins'

    
    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":  # ✅ Если это не главный процесс - выходим
            print("🚀 Первый запуск Django (игнорируем)")
            return
        print("Запускаем планировщик при старте Django")
        try:
            from .scheduler import start
            start()  # ✅ Запуск только при успешной загрузке Django
        except Exception as e:
            print(f"Ошибка при запуске планировщика: {e}")


# from django.apps import AppConfig
# import threading


# class CryptoCoinsConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "crypto_coins"

#     def ready(self):
#         if threading.active_count() > 1:
#             return  # 🚀 Избегаем двойного запуска в Django
#         print("✅ Запускаем планировщик при старте Django")
#         try:
#             from .scheduler import start
#             start()  # ✅ Запуск только при успешной загрузке Django
#         except Exception as e:
#             print(f"Ошибка при запуске планировщика: {e}")