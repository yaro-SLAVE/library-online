import asyncio
from django.conf import settings
from django.utils import timezone
from django.db.models import Prefetch, OuterRef, Subquery

from library_service.models.order import Order, OrderHistory
from library_service.emails import send_new_orders_summary_notification
from library_service.utils.datetime_helpers import is_working_hour

async def send_new_order_notifications_job_async():
    print("Job: Running async part of notification job.")
    
    email_mode = getattr(settings, 'EMAIL_MODE', 'prod')

    now = timezone.now()
    if email_mode == 'prod' and not is_working_hour(now):
        print("Job: Not a working hour and EMAIL_MODE is 'prod'. Skipping job.")
        return

    print("Job: It is a working hour (or EMAIL_MODE is not 'prod'). Proceeding...")
    print("Job: Searching for all orders with a current status of 'NEW'.")

    latest_status_subquery = OrderHistory.objects.filter(
        order=OuterRef('pk')
    ).order_by('-date').values('status')[:1]

    orders_to_notify = Order.objects.annotate(
        current_status=Subquery(latest_status_subquery)
    ).filter(
        current_status=OrderHistory.Status.NEW
    ).prefetch_related(
        'user',
        'library',
        Prefetch('statuses', queryset=OrderHistory.objects.order_by('date'))
    )

    orders_list = [order async for order in orders_to_notify]

    if not orders_list:
        print('Job: No orders with status NEW found.')
        return
        
    print(f'Job: Found {len(orders_list)} orders with status NEW to notify about.')
    
    try:
        await send_new_orders_summary_notification(orders_list, email_mode=email_mode)
        print(f'Job: Successfully processed notifications for {len(orders_list)} new orders.')
    except Exception as e:
        print(f"Job: An error occurred while processing notifications: {e}")

def send_new_order_notifications_job():
    print("Job: Kicking off notification job.")
    try:
        asyncio.run(send_new_order_notifications_job_async())
    except Exception as e:
        print(f"Job: Error in sync wrapper: {e}")
    print("Job: Finished notification job.")
