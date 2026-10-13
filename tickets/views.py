from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer, TicketStatusUpdateSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing support tickets.

    Provides standard CRUD endpoints:
    - POST   /api/tickets/                -> Create a ticket (201 Created)
    - GET    /api/tickets/                -> List tickets (supports ?status= and ?search=)
    - GET    /api/tickets/{id}/           -> Retrieve a single ticket (200 OK or 404 Not Found)
    - PUT    /api/tickets/{id}/           -> Fully update a ticket (200 OK or 400 Bad Request)
    - PATCH  /api/tickets/{id}/           -> Partially update a ticket (200 OK or 400 Bad Request)
    - DELETE /api/tickets/{id}/           -> Delete a ticket (204 No Content or 404 Not Found)

    Custom action:
    - PATCH  /api/tickets/{id}/update_status/ -> Update status only (open, in_progress, resolved)
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'email', 'name']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally filter tickets by status using ?status=<value>.
        """
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param.lower().strip())
        return queryset

    @action(detail=True, methods=['patch', 'post'], url_path='update_status')
    def update_status(self, request, pk=None):
        """
        Custom endpoint to update only the status of an existing ticket.
        Accepts: open, in_progress, or resolved.
        Rejects invalid statuses with HTTP 400.
        """
        ticket = self.get_object()
        serializer = TicketStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            ticket.status = serializer.validated_data['status']
            ticket.save(update_fields=['status', 'updated_at'])
            return Response(
                TicketSerializer(ticket).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
