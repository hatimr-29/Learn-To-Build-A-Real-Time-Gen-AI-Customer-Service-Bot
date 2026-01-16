# updater.py
from apscheduler.schedulers.background import BackgroundScheduler
from ingestion import update_database
import time

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_database, "interval", seconds=60)  # update every 60 sec
    scheduler.start()
    print("Auto-update scheduler started.")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Scheduler stopped.")
        scheduler.shutdown()
