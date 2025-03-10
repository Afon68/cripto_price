from apscheduler.schedulers.background import BackgroundScheduler
import atexit
# from datetime import datetime, timedelta,timezone
# # print("Этот принт стоит сразу после импорта в scheduler.py")
# # Глобальный флаг для проверки, запущен ли планировщик
# # scheduler_started = False

# def start():
#     # global scheduler_started
#     # print(scheduler_started)
#     # if scheduler_started:  # 🔥 Проверяем, не запущен ли уже планировщик
#     #     print("⚠ Планировщик уже работает, повторный запуск не требуется.")
#     #     return

#     # scheduler_started = True  # ✅ Теперь планировщик запущен

    
#     print("✅ Планировщик запущен!")  # 🔥 Проверка

#     from .services import price_token_from_rialto  # ✅ Импортируем `views.py` только внутри функции

#     scheduler = BackgroundScheduler()
#     # scheduler.add_job(price_token_from_rialto, 'date', run_date=(datetime.now() + timedelta(minutes=1)), id='price_token_from_rialto_1')
#     scheduler.add_job(price_token_from_rialto, "interval", seconds=60)     #  minutes=1  seconds=60  hours=1/20
#     scheduler.start()

#     # Останавливаем планировщик при завершении Django-сервера
#     atexit.register(lambda: scheduler.shutdown(wait=False))


def start():
    """Запуск Selenium при старте Django"""
    print("✅ Запускаем Selenium при старте Django...")
    
    # ✅ Запускаем Selenium в отдельном потоке
    import threading
    from .services import price_token_from_rialto
    threading.Thread(target=price_token_from_rialto, daemon=True).start()
    
    # Если нужны другие фоновые задачи, можно оставить планировщик
    scheduler = BackgroundScheduler()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown(wait=False))

# from apscheduler.schedulers.background import BackgroundScheduler
# import asyncio
# import threading
# from .fetch_token_price import run_all_tokens  # ✅ Импортируем асинхронную функцию

# def job_wrapper():
#     """Запускаем асинхронную функцию в новом потоке."""
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run_all_tokens())  # ✅ Теперь `asyncio.run()` не нужен

# def start():
#     """Запускаем планировщик в отдельном потоке."""
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(job_wrapper, "interval", minutes=1)  # 🔥 Асинхронная задача
#     scheduler.start()

#     # ✅ Запускаем планировщик в отдельном потоке, чтобы избежать ошибок `asyncio`
#     threading.Thread(target=scheduler.start, daemon=True).start()
#     print("✅ Планировщик запущен!")

#     # Останавливаем планировщик при завершении Django-сервера
#     atexit.register(lambda: scheduler.shutdown(wait=False))

   

