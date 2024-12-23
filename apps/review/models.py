from django.db import models
from django.db.models import UniqueConstraint, Q

from core.models import CoreModel


class Review(CoreModel):
    book = models.ForeignKey(
        "book.Book",
        on_delete=models.CASCADE
    )

    reviewer = models.ForeignKey(
        "membership.Profile",
        on_delete=models.CASCADE
    )

    review_text = models.TextField(

    )

    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['book', 'reviewer'],
                name='unique_active_review',
                condition=Q(is_active=True)
            )
        ]