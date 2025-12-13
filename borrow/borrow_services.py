from datetime import date
from borrow.models import Borrow
from notifications.telegram_services import (
    send_borrow_overdue_message,
    send_borrow_not_overdue_message,
)


def checking_overdue_borrows():
    queryset = Borrow.objects.filter(expected_return_date__lt=date.today()).filter(
        is_active=True
    )
    if queryset:
        for borrow in queryset:
            send_borrow_overdue_message(borrow)
    else:
        send_borrow_not_overdue_message()
