from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile model."""
    
    list_display = ['user', 'is_admin']
    list_filter = ['is_admin']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']
    ordering = ['user__username']
