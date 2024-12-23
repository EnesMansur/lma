from django.urls import path

from membership.api.views import *

urlpatterns = [
    path(
        'membership/',
        ProfileViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='membership-list'
    ),
    path(
        'membership/<int:pk>/',
        ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='membership-detail'
    ),
]
