from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def user_dashboard(request):
    """User page."""
    user = request.user
    return render(request, 'users/dashboard.html', {'user': user})
