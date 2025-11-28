from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import datetime

from .utils.datetime_helpers import is_working_hour, is_user_active_recently

from asgiref.sync import sync_to_async

async def send_new_orders_summary_notification(orders, email_mode='prod'):
    print("Email: Starting summary notification process.")
    now = datetime.now()
    
    if not is_working_hour(now) and email_mode == 'prod':
        print("Email: Not a working hour and email_mode is 'prod'. Skipping.")
        return

    try:
        librarian_group = await Group.objects.aget(name='Librarian')
        librarians_qs = get_user_model().objects.filter(groups=librarian_group)
        librarians_list = [l async for l in librarians_qs]
        print(f"Email: Found {len(librarians_list)} librarians in 'Librarian' group.")

    except Group.DoesNotExist:
        print("Email: 'Librarian' group not found. Cannot send notifications.")
        return

    email_details = {}
    if orders:
        subject = f"Сейчас в системе {len(orders)} новых заказов"
        plain_message = f"Здравствуйте, [LIBRARIAN_NAME].\n\n"
        plain_message += f"В системе {len(orders)} новых заказов. Пожалуйста, проверьте систему.\n\n"
        plain_message += "Детали заказов:\n"
        for order in orders:
            creation_date_info = "N/A"
            if order.statuses.exists():
                creation_date_info = order.statuses.all()[0].date.strftime("%Y-%m-%d %H:%M:%S")
            
            plain_message += f"- Заказ #{order.id} от {order.user.email} (Создан: {creation_date_info})\n"
        
        email_details = {
            'subject': subject,
            'body': plain_message,
            'from_email': settings.DEFAULT_FROM_EMAIL,
        }

    if email_mode == 'off':
        if email_details:
            print("Email: EMAIL_MODE is 'off'. Printing to console:")
            for librarian in librarians_list:
                if is_user_active_recently(librarian):
                    final_body = email_details['body'].replace("[LIBRARIAN_NAME]", librarian.get_full_name() or librarian.username)
                    print(f"--- Console Email to {librarian.email} ---")
                    print(f"Subject: {email_details['subject']}")
                    print(f"Body:\n{final_body}")
                    print("-----------------------------")
        else:
            print("Email: EMAIL_MODE is 'off', no orders to notify.")
        return

    for librarian in librarians_list:
        if is_user_active_recently(librarian):
            print(f"Email: Sending to {librarian.email} (active).")
            try:
                final_body = email_details['body'].replace("[LIBRARIAN_NAME]", librarian.get_full_name() or librarian.username)
                
                await sync_to_async(send_mail)(
                    email_details['subject'],
                    final_body,
                    email_details['from_email'],
                    [librarian.email],
                    fail_silently=False,
                )
                print(f"Email: Successfully sent to {librarian.email}.")
            except Exception as e:
                print(f"Email: Error sending to {librarian.email}: {e}")
                pass
        else:
            print(f"Email: Skipping {librarian.email} (not active).")



