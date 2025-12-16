import decimal
import os
from decimal import Decimal
from typing import Callable

import stripe
from django.http import HttpRequest
from django.urls import reverse

from borrow.models import Borrow
from payments.models import Payment


def create_checkout_session(
    instance: Borrow,
    request: HttpRequest,
    type_of_payment: str,
    amount_to_pay: Callable[[Borrow], decimal],
) -> str:

    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    amount_to_pay = amount_to_pay(instance)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{instance.book.title} by {instance.book.author}",
                    },
                    "unit_amount": amount_to_pay * 100,
                },
                "quantity": 1,
            }
        ],
        metadata={"type_of_payment": type_of_payment},
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payment:cancel"))
        + "?session_id={CHECKOUT_SESSION_ID}",
    )

    create_payment(
        instance=instance, strip_session=checkout_session, amount_to_pay=amount_to_pay
    )

    return checkout_session.url


def total_amount(instance: Borrow) -> int:
    delta = instance.expected_return_date - instance.borrow_date
    count_days = delta.days
    sum_for_pay = instance.book.daily_fee * count_days
    return int(sum_for_pay)


def set_status_paid(session_id: str) -> None:
    payment = Payment.objects.get(session_id=session_id)
    payment.status = "paid"
    payment.type = "payment"
    payment.save()


def create_payment(
    instance: Borrow,
    strip_session: stripe.checkout.Session,
    amount_to_pay: Decimal,
) -> None:
    Payment.objects.create(
        borrowing=instance,
        session_url=strip_session.url,
        session_id=strip_session.id,
        money_to_pay=amount_to_pay,
    )


def calculate_fine_amount(instance: Borrow) -> int:
    fine_multiplier = 2
    delta = instance.actual_return_date - instance.expected_return_date
    count_days = delta.days
    sum_for_pay = instance.book.daily_fee * count_days * fine_multiplier
    return int(sum_for_pay)


def set_type_fine(session_id: str) -> None:
    payment = Payment.objects.get(session_id=session_id)
    payment.status = "paid"
    payment.type = "fine"
    payment.save()
