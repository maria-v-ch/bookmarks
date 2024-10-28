"""URL configuration for the account application."""

from django.contrib.auth import views as auth_views
from django.urls import include, path
from . import views

app_name = 'account'

urlpatterns = [
    # Password reset URLs
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url='done/'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url='/account/reset/done/'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    
    # Authentication URLs
    path('', include('django.contrib.auth.urls')),
    
    # Dashboard URLs
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Registration and profile URLs
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    
    # Admin management URLs
    path(
        'make-admin/<int:user_id>/',
        views.make_admin,
        name='make_admin'
    ),
    path(
        'remove-admin/<int:user_id>/',
        views.remove_admin,
        name='remove_admin'
    ),
]
