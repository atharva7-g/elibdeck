from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from allauth.account.views import LoginView

# Create your views here.
@login_required
def user_dashboard(request):
    """User page."""
    user = request.user
    return render(request, 'users/dashboard.html', {'user': user})

class LibrarianLoginView(LoginView):
    template_name = 'users/librarian_login.html'
    success_url = reverse_lazy('profile-page')