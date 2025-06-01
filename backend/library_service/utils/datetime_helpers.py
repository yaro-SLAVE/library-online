from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

def is_working_hour(dt: datetime) -> bool:
    day = dt.weekday()
    hour = dt.hour

    if settings.DAYS['MONDAY'] <= day <= settings.DAYS['FRIDAY']:
        return settings.WORKING_HOURS['MONDAY_TO_FRIDAY_START_HOUR'] <= hour < settings.WORKING_HOURS['MONDAY_TO_FRIDAY_END_HOUR']
    elif day == settings.DAYS['SATURDAY']:
        return settings.WORKING_HOURS['SATURDAY_START_HOUR'] <= hour < settings.WORKING_HOURS['SATURDAY_END_HOUR']
    return False

def is_user_active_recently(user) -> bool:
    if not user.is_authenticated or not user.last_login:
        return False

    now_aware = timezone.now()
    time_since_last_login = now_aware - user.last_login

    active_threshold = timedelta(hours=2)

    return time_since_last_login <= active_threshold