# urls.py
from django.urls import path
from .views import MediaSearchView

urlpatterns = [
    path('search/', MediaSearchView.as_view(), name='search_media'),
]
