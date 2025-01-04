from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.user_dashboard, name='profile-page'),
    path('librarian/login/', views.LibrarianLoginView.as_view(), name='librarian-login'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
]