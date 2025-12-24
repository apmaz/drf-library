from django.db import models
from borrow.models import Borrow


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "payment"
        FINE = "fine"

    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=20
    )
    type = models.CharField(
        choices=TypeChoices.choices, default=None, null=True, blank=True, max_length=20
    )
    borrowing = models.ForeignKey(
        Borrow, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.TextField(null=True, blank=True)
    session_id = models.TextField(null=True, blank=True)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return f"ID: {self.pk}, borrow_id: {self.borrowing.id}, Money_to_pay: {self.money_to_pay}"
