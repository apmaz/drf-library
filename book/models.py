from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "hard",
        SOFT = "soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=CoverChoices.choices)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    daily_fee = models.DecimalField(max_digits=6, decimal_places=3)

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
