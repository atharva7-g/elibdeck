from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def user_dashboard(request):
    """User page."""
    user = request.user
    return render(request, 'users/dashboard.html', {'user': user})

def librarian_login(request):
    if request.user.is_authenticated and request.user.is_librarian:
        return redirect('/')  # Redirect if already logged in
    return render(request, 'users/librarian_login.html')
