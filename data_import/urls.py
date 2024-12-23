from django.urls import path
from . import views

app_name = 'data_import'

urlpatterns = [
    path('', views.upload_file, name='book-list-upload'),
]