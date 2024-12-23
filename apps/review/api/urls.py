from django.urls import path

from review.api.views import *

urlpatterns = [
    path(
        'review/',
        ReviewListViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='review-list'
    ),
    path(
        'review/<int:pk>/',
        ReviewListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='review-detail'
    ),
]
