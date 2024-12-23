from django.urls import path, include

urlpatterns = [
    path('books/', include('book.api.urls')),
    path('borrow/', include('borrow.api.urls')),
    path('review/', include('review.api.urls')),
    path('membership/', include('membership.api.urls')),
]
