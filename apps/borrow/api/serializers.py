from rest_framework import serializers
from borrow.models import BorrowRecord


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ["member", "book_edition", "due_date", "return_date"]
