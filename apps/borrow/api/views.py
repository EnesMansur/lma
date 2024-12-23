from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from borrow.models import BorrowRecord
from .serializers import BorrowSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from membership.models import Profile
from rest_framework.exceptions import ValidationError

import django_filters
from datetime import date


class BorrowRecordFilterSet(django_filters.FilterSet):
    """
    gecikmis leri ozel olarak filtre yap
    """
    overdue = django_filters.BooleanFilter(method='filter_overdue', label='Gecikmiş Mi(true/false)')

    def filter_overdue(self, queryset, name, value):
        if value is not None:
            if str(value) in ["true", "True", "1"]:
                return queryset.filter(due_date__lt=date.today(), return_date__isnull=True)
            else:
                return queryset.exclude(due_date__lt=date.today(), return_date__isnull=True)
        return queryset

    class Meta:
        model = BorrowRecord
        fields = ['member', 'book_edition']


class BorrowListViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'member__user__first_name',
        'member__user__last_name',
        'book_edition__edition_number',
        'book_edition__book__title',
        'book_edition__book__author',
        'book_edition__book__isbn',
    ]
    ordering_fields = ['book_edition__book__publication_date']
    ordering = ['book_edition__book__publication_date']  # default
    filterset_class = BorrowRecordFilterSet  #ozel filtre. sadece gecikenleri gormek isteyebiliriz

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = request.data
        membership_id = data.get("member")
        member_obj = Profile.objects.get(id=membership_id)
        result, detail = member_obj.can_booking()
        if not result:
            raise ValidationError(str(detail))

        response_data = serializer.data
        response_data['id'] = serializer.instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)

