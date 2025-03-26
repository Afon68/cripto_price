import atexit
from apscheduler.schedulers.background import BackgroundScheduler




def start():
    print("✅ Планировщик запущен!")  # 🔥 Проверка

    from .write_to_db import write_to_db  # ✅ Импортируем `write_to_db' только внутри функции

    scheduler = BackgroundScheduler()
    scheduler.add_job(write_to_db, "interval", hours=1/60)
    scheduler.start()

    # Останавливаем планировщик при завершении Django-сервера
    atexit.register(lambda: scheduler.shutdown(wait=False))


   

