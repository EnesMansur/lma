from django.db import models
from core.models import CoreModel
from django.utils.translation import gettext_lazy as _
from enum import Enum


class FormatEnum(str, Enum):
    HARDCOVER = "Hardcover"
    PAPERBACK = "Paperback"
    EBOOK = "eBook"
    OTHER = "Other"

    @classmethod
    def choose_list(cls):
        return [[c.value, _(c.name.capitalize())] for c in cls]


class Book(CoreModel):
    title = models.CharField(
        max_length=64
    )

    author = models.CharField(
        max_length=32
    )

    publication_date = models.DateField()

    isbn = models.CharField(
        unique=True,
        db_index=True,
        max_length=32,
    )

    genre = models.CharField(
        max_length=100,
        null=True, blank=True
    )

    quantity = models.IntegerField(default=0)


class BookEdition(CoreModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    edition_number = models.IntegerField(

    )

    published_year = models.IntegerField(

    )

    quantity = models.IntegerField(
        default=0
    )

    format = models.CharField(
        max_length=50,
        choices=FormatEnum.choose_list(),
        default=FormatEnum.OTHER

    )
