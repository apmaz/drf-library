from django.db import models
from django.core.exceptions import ValidationError
from book.models import Book
from drf_library import settings


class Borrow(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrows_books"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrows_user"
    )

    def decrease_one_from_borrow_book_inventory(self):
        self.book.decrease_one_from_inventory()

    def clean(self):
        super().clean()
        if self.borrow_date >= self.expected_return_date:
            raise ValidationError(
                "Expected return date can't be before or equal to the borrow date"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        self.decrease_one_from_borrow_book_inventory()
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Borrow date - {self.borrow_date}, "
            f"Exp. return date - {self.expected_return_date}, "
            f"book - {self.book}, "
            f"user - {self.user}"
        )
