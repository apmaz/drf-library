from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "hard",
        SOFT = "soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=CoverChoices.choices)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=6, decimal_places=3)

    def decrease_on_1_for_inventory(self):
        if self.inventory == 0:
            raise ValidationError("The inventory of this book is 0")
        self.inventory -= 1
        self.save()

    def increase_on_1_for_inventory(self):
        self.inventory += 1
        self.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author", "cover"],
                name="unique_title_author_cover",
            ),
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"
