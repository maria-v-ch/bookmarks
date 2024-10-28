"""Views for the account application."""

from typing import Optional

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, UserRegistrationForm, UserEditForm
from .models import Profile

User = get_user_model()


def user_login(request: HttpRequest) -> HttpResponse:
    """Handle user login with username/email and password."""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('account:dashboard')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account:dashboard')
                messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request: HttpRequest) -> HttpResponse:
    """Handle new user registration."""
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered and logged in.')
        return redirect('account:dashboard')
        
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Display user dashboard."""
    if request.user.profile.is_admin:
        return redirect('account:admin_dashboard')
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    """Handle user profile editing."""
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request,
        'account/edit.html',
        {'user_form': user_form}
    )


def is_admin(user: User) -> bool:
    """Check if user has admin privileges."""
    return user.is_authenticated and user.profile.is_admin


@user_passes_test(is_admin)
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    """Display admin dashboard."""
    users = User.objects.all()
    return render(request, 'account/admin_dashboard.html', {'users': users})


@login_required
def make_admin(request: HttpRequest, user_id: int) -> HttpResponse:
    """Promote a user to admin status."""
    if request.user.profile.is_admin:
        user_to_promote = User.objects.get(id=user_id)
        user_to_promote.profile.make_admin()
        messages.success(
            request,
            f'{user_to_promote.username} has been made an admin.'
        )
    else:
        messages.error(
            request,
            'You do not have permission to perform this action.'
        )
    return redirect('account:dashboard')


@login_required
def remove_admin(request: HttpRequest, user_id: int) -> HttpResponse:
    """Remove admin status from a user."""
    if request.user.profile.is_admin:
        user_to_demote = User.objects.get(id=user_id)
        user_to_demote.profile.remove_admin()
        messages.success(
            request,
            f'{user_to_demote.username} has been removed as an admin.'
        )
    else:
        messages.error(
            request,
            'You do not have permission to perform this action.'
        )
    return redirect('account:dashboard')
