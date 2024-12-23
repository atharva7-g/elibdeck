from django.urls import path
from . import views

app_name = 'books_catalog'

urlpatterns = [
    path('', views.upload_file, name='book-list-upload'),
]