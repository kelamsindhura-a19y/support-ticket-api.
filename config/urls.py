"""
URL configuration for Support Ticket Management System.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def root_view(request):
    """Friendly root endpoint guiding users to available APIs."""
    return JsonResponse({
        "message": "Welcome to Support Ticket Management System API",
        "endpoints": {
            "tickets_list_and_create": "/api/tickets/",
            "ticket_detail_example": "/api/tickets/<id>/",
            "ticket_update_status_example": "/api/tickets/<id>/update_status/",
            "admin_dashboard": "/admin/"
        },
        "instructions": "Visit /api/tickets/ to test endpoints interactively in your browser or Postman."
    })


urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('tickets.urls')),
]

