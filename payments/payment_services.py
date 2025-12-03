import os
import stripe
from borrow.models import Borrow
from payments.models import Payment


def create_checkout_session(instance: Borrow) -> str:
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
        success_url="http://localhost:4242/success",
    )

    Payment.objects.create(
        borrowing=instance,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=sum_to_pay,
    )

    return checkout_session.url


def total_amount(instance: Borrow):
    delta = instance.expected_return_date - instance.borrow_date
    count_days = delta.days
    sum_for_pay = instance.book.daily_fee * count_days
    return int(sum_for_pay)
