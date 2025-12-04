import os
import stripe
from django.shortcuts import render
from django.urls import reverse

from borrow.models import Borrow
from payments.models import Payment


def create_checkout_session(instance: Borrow, request) -> str:
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    sum_to_pay = total_amount(instance)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{instance.book.title} by {instance.book.author}",
                    },
                    "unit_amount": sum_to_pay * 100,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payment:cancel"))
        + "?session_id={CHECKOUT_SESSION_ID}",
    )

    Payment.objects.create(
        borrowing=instance,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=sum_to_pay,
    )

    print(checkout_session.url)


def total_amount(instance: Borrow):
    delta = instance.expected_return_date - instance.borrow_date
    count_days = delta.days
    sum_for_pay = instance.book.daily_fee * count_days
    return int(sum_for_pay)


def success(request):
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    customer = session.customer
    set_status_paid(session_id)
    return render(request, "success.html", {"customer": customer})


def cancel(request):
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    customer = session.customer
    return render(request, "cancel.html", {"customer": customer})


def set_status_paid(session_id: str):
    Payment.objects.filter(session_id=session_id).update(status="paid")
