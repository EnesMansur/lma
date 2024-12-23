from django.db import models
from core.models import CoreModel


class BorrowRecord(CoreModel):
    member = models.ForeignKey(
        "membership.Profile",
        on_delete=models.CASCADE
    )

    book_edition = models.ForeignKey(
        "book.BookEdition",
        on_delete=models.CASCADE
    )

    borrow_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField()
    return_date = models.DateField(
        null=True, blank=True
    )
