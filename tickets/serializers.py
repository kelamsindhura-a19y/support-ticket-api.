from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for Ticket model.
    Handles serialization and validation for CRUD operations.
    """
    status = serializers.ChoiceField(
        choices=Ticket.StatusChoices.choices,
        default=Ticket.StatusChoices.OPEN,
        error_messages={
            'invalid_choice': 'Invalid status. Allowed choices are: open, in_progress, resolved.'
        }
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'name',
            'email',
            'title',
            'description',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': 'Name cannot be blank.',
                    'required': 'Name is required.',
                    'max_length': 'Name cannot exceed 100 characters.',
                }
            },
            'email': {
                'error_messages': {
                    'blank': 'Email cannot be blank.',
                    'required': 'Email is required.',
                    'invalid': 'Enter a valid email address.',
                }
            },
            'title': {
                'error_messages': {
                    'blank': 'Title cannot be blank.',
                    'required': 'Title is required.',
                    'max_length': 'Title cannot exceed 200 characters.',
                }
            },
            'description': {
                'error_messages': {
                    'blank': 'Description cannot be blank.',
                    'required': 'Description is required.',
                }
            },
        }

    def validate_name(self, value):
        trimmed = value.strip()
        if not trimmed:
            raise serializers.ValidationError("Name cannot be blank or contain only whitespace.")
        return trimmed

    def validate_title(self, value):
        trimmed = value.strip()
        if not trimmed:
            raise serializers.ValidationError("Title cannot be blank or contain only whitespace.")
        return trimmed

    def validate_description(self, value):
        trimmed = value.strip()
        if not trimmed:
            raise serializers.ValidationError("Description cannot be blank or contain only whitespace.")
        return trimmed


class TicketStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer specifically for updating ticket status via the custom action.
    """
    status = serializers.ChoiceField(
        choices=Ticket.StatusChoices.choices,
        error_messages={
            'required': 'The status field is required.',
            'invalid_choice': 'Invalid status. Allowed choices are: open, in_progress, resolved.'
        }
    )
