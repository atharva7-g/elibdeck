from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.user_dashboard, name='profile-page'),
    path('librarian/login', views.librarian_login, name='librarian-login'),
]