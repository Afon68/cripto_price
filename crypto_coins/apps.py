from django.apps import AppConfig
import os


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


