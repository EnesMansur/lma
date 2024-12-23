from django.urls import path, include

from book.api.views import *

urlpatterns = [
    # book
    path(
        'books/bulk/dummy/creaet/',
        BookBulkDummyViewSet.as_view(),
        name='book-bulk'
    ),

    path(
        'books/list/',
        BookListViewSet.as_view(),
        name='book-list-sql'
    ),

    path(
        'books/',
        BookViewSet.as_view({'post': 'create'}),
        name='book-list'
    ),
    path(
        'books/<int:pk>/',
        BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='book-detail'
    ),

    # BookEdition
    path(
        'edition/books/bulk/dummy/creaet/',
        EditionBookBulkDummyViewSet.as_view(),
        name='edition-bulk'
    ),

    path(
        'edition/books/',
        EditionBookListViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='edition-list'
    ),
    path(
        'edition/books/<int:pk>/',
        EditionBookListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='edition-detail'
    ),
]
