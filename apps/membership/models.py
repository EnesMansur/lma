from django.contrib.auth.models import User
from django.db import models
from core.models import CoreModel
from django.utils.translation import gettext_lazy as _
from enum import Enum
from borrow.models import BorrowRecord
import datetime


class RoleEnum(str, Enum):
    ADMIN = "Admin"
    MEMBER = "Member"

    @classmethod
    def choose_list(cls):
        return [[c.value, _(c.name.capitalize())] for c in cls]


class Profile(CoreModel):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )

    role = models.CharField(
        max_length=32,
        choices=RoleEnum.choose_list(),
        default=RoleEnum.MEMBER,
    )

    def can_booking(self):
        """
        *Rules*
        - A member can borrow a maximum of 5 books at a time.
        - If a book is overdue, an error should be raised when attempting to borrow another.
        """

        result, detail = self.check_booking_borrowing()
        # geciken yoksa. ek sorgu yapmayalim
        if result:
            result, detail = self.check_booking_limit()
        return result, detail

    def check_booking_limit(self):
        """
        A member can borrow a maximum of 5 books at a time.
        """
        result = True
        detail = None
        if self.borrowrecord_set.filter(
                is_active=True,
                return_date__isnull=True
        ).count() >= 5:
            result = False
            detail = "max 5 kitap alabilirsiniz"
        return result, detail

    def check_booking_borrowing(self):
        result = True
        detail = None
        if BorrowRecord.objects.filter(
                is_active=True,
                member=self,
                due_date__lt=datetime.datetime.now(),
                return_date__isnull=True
        ).exists():
            result = False
            detail = "Geçikmede kitabnız var. yeni kitap alamazsınız"

        return result, detail

    def can_review(self, book_id):
        """
         *Rules*
         - Members can only review books they have borrowed.
        """
        result = True
        detail = None
        if not self.borrowrecord_set.filter(
                is_active=True,
                return_date__isnull=False,  # teslim etmis olmali
                book_edition__book__id=book_id
        ).exists():
            result = False
            detail = "Sadece kendi kitap rezervasyonları değerlendirebilirsin"
        return result, detail
