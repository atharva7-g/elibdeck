from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from allauth.account.views import LoginView
from django.contrib import messages
from .forms import EditUserForm


# Create your views here.
@login_required
def user_dashboard(request):
    """User page."""
    user = request.user

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  # Redirect to avoid resubmission issues
    else:
        form = EditUserForm(instance=user)

    return render(request, 'users/dashboard.html', {'user': user})


class LibrarianLoginView(LoginView):
    template_name = 'users/librarian_login.html'


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!', extra_tags='edit-profile-success')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'users/edit_user.html', {'form': form})
