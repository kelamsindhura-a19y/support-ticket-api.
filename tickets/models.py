from django.db import models


class Ticket(models.Model):
    """
    Support Ticket Model.
    Stores customer support requests with contact info, status, and timestamps.
    """

    class StatusChoices(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'

    name = models.CharField(
        max_length=100,
        help_text="Name of the person submitting the ticket (max 100 characters)."
    )
    email = models.EmailField(
        help_text="Valid email address of the requester."
    )
    title = models.CharField(
        max_length=200,
        help_text="Summary or title of the issue (max 200 characters)."
    )
    description = models.TextField(
        help_text="Detailed explanation of the issue."
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN,
        help_text="Current status of the ticket: open, in_progress, or resolved."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the ticket was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the ticket was last updated."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'

    def __str__(self):
        return f"Ticket #{self.id}: {self.title} [{self.status}]"
