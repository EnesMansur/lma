from django.urls import path

from borrow.api.views import *

urlpatterns = [
    path(
        'borrow/',
        BorrowListViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='borrow-list'
    ),
    path(
        'borrow/<int:pk>/',
        BorrowListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='borrow-detail'
    ),
]
