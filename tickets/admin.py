from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ticket model.
    Provides clear list view, filtering, and search capabilities.
    """
    list_display = (
        'id',
        'title',
        'name',
        'email',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'name', 'email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
