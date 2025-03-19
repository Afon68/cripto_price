from apscheduler.schedulers.background import BackgroundScheduler
import atexit



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



   

