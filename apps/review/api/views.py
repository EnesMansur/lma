from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from membership.models import Profile
from review.models import Review
from .serializers import ReviewSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from api.views import CustomResponse

class ReviewListViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'reviewer__user__first_name',
        'reviewer__user__last_name',
        'book__title',
        'book__author',
        'book__isbn',
        'rating'
    ]
    ordering_fields = ['book__publication_date']
    ordering = ['book__publication_date']  # default

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = request.data
        book_id = data.get("book")
        membership_id = data.get("reviewer")
        member_obj = Profile.objects.get(id=membership_id)
        result, detail = member_obj.can_review(book_id=book_id)
        if not result:
            return CustomResponse(
                data=None,
                message=detail,
                status_code=status.HTTP_403_FORBIDDEN

            )

        response_data = serializer.data
        response_data['id'] = serializer.instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)

