from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import datetime

from .utils.datetime_helpers import is_working_hour, is_user_active_recently

from asgiref.sync import sync_to_async

async def send_new_order_notification():
    now = datetime.now()
    if not is_working_hour(now): 
        return

    try:
        librarian_group = await Group.objects.aget(name='Librarian')
        librarians = get_user_model().objects.filter(groups=librarian_group)
    except Group.DoesNotExist:
        return

    notified_count = 0


    async for librarian in librarians: 
        if is_user_active_recently(librarian):
            try:
                context = {}
                subject = "У вас новый заказ!"
                html_message = await sync_to_async(render_to_string)('emails/new_order_notification.html', context)
                plain_message = "У вас новый заказ! Пожалуйста, проверьте систему."

                email = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [librarian.email]
                )
                await sync_to_async(email.attach_alternative)(html_message, "text/html")
                await sync_to_async(email.send)(fail_silently=False)
                notified_count += 1
            except Exception as e:
                return
