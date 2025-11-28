import os
from django.apps import AppConfig
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import send_new_order_notifications_job        
import library_service.signals

class LibraryServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library_service"

    def ready(self):
        
        if os.environ.get('RUN_MAIN'):

            scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
            
            interval_seconds = getattr(settings, 'NOTIFICATION_SCHEDULER_INTERVAL_SECONDS', 3600)

            scheduler.add_job(
                send_new_order_notifications_job,
                'interval',
                seconds=interval_seconds,
                id='send_new_order_notifications_job',
                replace_existing=True
            )
            
            print(f"--- Starting BackgroundScheduler. Job interval: {interval_seconds} seconds. ---")
            scheduler.start()
