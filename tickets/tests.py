from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Ticket


class TicketAPITests(APITestCase):
    """
    Automated test suite for the Support Ticket Management System REST APIs.
    Covers all CRUD endpoints, custom status updates, filtering, searching, and validation.
    """

    def setUp(self):
        """Set up initial test data."""
        self.ticket1 = Ticket.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            title="Cannot login to portal",
            description="Getting a 500 error when clicking the login button on Chrome.",
            status=Ticket.StatusChoices.OPEN
        )
        self.ticket2 = Ticket.objects.create(
            name="Bob Smith",
            email="bob@example.com",
            title="Invoice download fails",
            description="The PDF invoice is corrupted upon downloading.",
            status=Ticket.StatusChoices.IN_PROGRESS
        )
        self.ticket3 = Ticket.objects.create(
            name="Charlie Brown",
            email="charlie@example.com",
            title="Password reset link expired",
            description="The reset token expired within 1 minute instead of 24 hours.",
            status=Ticket.StatusChoices.RESOLVED
        )

        self.list_create_url = reverse('ticket-list')
        self.detail_url_1 = reverse('ticket-detail', kwargs={'pk': self.ticket1.pk})
        self.nonexistent_url = reverse('ticket-detail', kwargs={'pk': 99999})
        self.update_status_url_1 = reverse('ticket-update-status', kwargs={'pk': self.ticket1.pk})

    # 1. Create a ticket (POST /api/tickets/)
    def test_create_ticket_success(self):
        """Test successfully creating a ticket with valid data."""
        payload = {
            "name": "Diana Prince",
            "email": "diana@example.com",
            "title": "Payment gateway timeout",
            "description": "Stripe webhook failed to confirm payment."
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(response.data['email'], payload['email'])
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['description'], payload['description'])
        self.assertEqual(response.data['status'], Ticket.StatusChoices.OPEN)
        self.assertIn('id', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)

        # Verify database persistence
        self.assertTrue(Ticket.objects.filter(id=response.data['id']).exists())

    # 2. Reject missing required fields
    def test_create_ticket_missing_required_fields(self):
        """Test that creating a ticket without required fields returns HTTP 400."""
        payload = {}
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)

    def test_create_ticket_blank_fields_rejected(self):
        """Test that blank strings or whitespace-only inputs are rejected with HTTP 400."""
        payload = {
            "name": "   ",
            "email": "valid@example.com",
            "title": "   ",
            "description": "   "
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)

    # 3. Reject invalid email address
    def test_create_ticket_invalid_email(self):
        """Test that submitting an invalid email address returns HTTP 400."""
        payload = {
            "name": "Bruce Wayne",
            "email": "not-an-email",
            "title": "Batmobile GPS broken",
            "description": "The GPS keeps routing through Arkham Asylum."
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    # 4. List all tickets (GET /api/tickets/)
    def test_list_tickets(self):
        """Test listing all tickets returns HTTP 200 and all items."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_tickets_by_status(self):
        """Test optional filtering tickets by status query parameter."""
        response = self.client.get(f"{self.list_create_url}?status=open")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'open')

        # Test filtering for in_progress
        response_ip = self.client.get(f"{self.list_create_url}?status=in_progress")
        self.assertEqual(response_ip.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_ip.data), 1)
        self.assertEqual(response_ip.data[0]['status'], 'in_progress')

    def test_search_tickets(self):
        """Test searching tickets by keyword in title/email/name."""
        response = self.client.get(f"{self.list_create_url}?search=Invoice")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Invoice download fails")

    # 5. Retrieve one ticket (GET /api/tickets/{id}/)
    def test_retrieve_ticket_success(self):
        """Test retrieving a single ticket by its ID."""
        response = self.client.get(self.detail_url_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.ticket1.id)
        self.assertEqual(response.data['title'], self.ticket1.title)

    # 6. Retrieve nonexistent ticket (GET /api/tickets/99999/)
    def test_retrieve_ticket_not_found(self):
        """Test retrieving a nonexistent ticket returns HTTP 404."""
        response = self.client.get(self.nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 7. Update ticket (PUT /api/tickets/{id}/)
    def test_update_ticket_full_success(self):
        """Test full update of all ticket fields via PUT."""
        payload = {
            "name": "Alice Johnson Updated",
            "email": "alice.new@example.com",
            "title": "Cannot login to portal - Solved with cache clear",
            "description": "User confirmed clearing cookies resolved the issue.",
            "status": "resolved"
        }
        response = self.client.put(self.detail_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(response.data['status'], 'resolved')

        # Verify DB updated
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.name, payload['name'])
        self.assertEqual(self.ticket1.status, 'resolved')

    def test_update_ticket_missing_field_rejected(self):
        """Test that PUT with missing required field is rejected with HTTP 400."""
        payload = {
            "name": "Alice Johnson Updated",
            # missing email, title, description
        }
        response = self.client.put(self.detail_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 8. Partially update ticket (PATCH /api/tickets/{id}/)
    def test_partial_update_ticket_success(self):
        """Test updating only selected fields via PATCH."""
        payload = {
            "title": "New Updated Title Only"
        }
        response = self.client.patch(self.detail_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "New Updated Title Only")
        # Ensure other fields were not overwritten
        self.assertEqual(response.data['email'], self.ticket1.email)

    # 9. Reject invalid status
    def test_partial_update_invalid_status_rejected(self):
        """Test that updating status to an invalid value via PATCH returns HTTP 400."""
        payload = {
            "status": "closed_forever"
        }
        response = self.client.patch(self.detail_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    # 10. Custom action: Update ticket status (PATCH /api/tickets/{id}/update_status/)
    def test_custom_action_update_status_success(self):
        """Test custom action PATCH /api/tickets/{id}/update_status/ with valid status."""
        payload = {"status": "in_progress"}
        response = self.client.patch(self.update_status_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'in_progress')

        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, 'in_progress')

        # Transition to resolved
        payload = {"status": "resolved"}
        response = self.client.patch(self.update_status_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'resolved')

    def test_custom_action_update_status_invalid_rejected(self):
        """Test custom action rejects invalid status choices with HTTP 400."""
        payload = {"status": "archived"}
        response = self.client.patch(self.update_status_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_custom_action_update_status_missing_status(self):
        """Test custom action rejects missing status field with HTTP 400."""
        payload = {}
        response = self.client.patch(self.update_status_url_1, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_custom_action_nonexistent_ticket(self):
        """Test custom action on nonexistent ticket returns HTTP 404."""
        url = reverse('ticket-update-status', kwargs={'pk': 99999})
        response = self.client.patch(url, {"status": "resolved"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 11. Delete ticket (DELETE /api/tickets/{id}/)
    def test_delete_ticket_success(self):
        """Test deleting an existing ticket returns HTTP 204."""
        response = self.client.delete(self.detail_url_1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.filter(id=self.ticket1.id).exists())

    def test_delete_ticket_not_found(self):
        """Test deleting a nonexistent ticket returns HTTP 404."""
        response = self.client.delete(self.nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
