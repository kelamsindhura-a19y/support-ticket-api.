# Support Ticket Management System — Backend Developer Internship

A robust, production-ready RESTful backend API for managing customer support requests, built with **Python**, **Django**, and **Django REST Framework (DRF)** using an **SQLite** database.

---

## 1. Project Overview

The **Support Ticket Management System** allows users to submit support issues and enables administrators and support engineers to manage tickets throughout their lifecycle (`open` &rarr; `in_progress` &rarr; `resolved`).

### Key Features
- **Full CRUD Operations**: Create, read (list and single view), full update (PUT), partial update (PATCH), and delete (DELETE) tickets.
- **Custom Status Management**: Dedicated endpoint (`PATCH /api/tickets/{id}/update_status/`) to update status with strict choice validation.
- **Advanced Filtering & Search**: Query tickets by status (e.g., `?status=open`) or search by title, email, or name (e.g., `?search=login`).
- **Comprehensive Validation & Error Handling**: User-friendly, field-specific validation messages with standard HTTP status codes (`200`, `201`, `204`, `400`, `404`).
- **Django Admin Panel**: Integrated administration interface for browsing, filtering, and managing tickets.
- **Automated Testing**: 19 automated unit and integration tests covering all endpoints and edge cases.

---

## 2. Technology Stack

- **Language:** Python 3.10+ (tested with Python 3.14)
- **Framework:** Django 5.x / 6.x
- **API Toolkit:** Django REST Framework (DRF) 3.15+
- **Database:** SQLite3 (zero-configuration file database)
- **Testing Tools:** Django REST Framework `APITestCase`, Postman
- **Platform:** Windows / Linux / macOS (Windows PowerShell instructions provided)

---

## 3. Project Structure

```text
support_ticket/
│
├── manage.py                   # Django CLI management utility
├── requirements.txt            # Project dependencies
├── README.md                   # Comprehensive documentation & guide
├── .gitignore                  # Git ignore rules for Python/Django/OS
│
├── config/                     # Project configuration directory
│   ├── __init__.py
│   ├── settings.py             # Django & DRF settings
│   ├── urls.py                 # Root URL routing (routes /api/ to tickets app)
│   ├── wsgi.py                 # WSGI application entrypoint
│   └── asgi.py                 # ASGI application entrypoint
│
└── tickets/                    # Application directory
    ├── __init__.py
    ├── admin.py                # Django admin configuration
    ├── apps.py                 # Application configuration
    ├── models.py               # Ticket database model
    ├── serializers.py          # DRF serializers (TicketSerializer, TicketStatusUpdateSerializer)
    ├── views.py                # TicketViewSet with standard actions and custom status update
    ├── urls.py                 # App URL routing using DefaultRouter
    ├── tests.py                # 19 automated unit & integration tests
    └── migrations/
        ├── __init__.py
        └── 0001_initial.py     # Initial database migration
```

---

## 4. Understanding the Request Lifecycle (Beginner Guide)

Here is how a request travels through the application:

```
[Postman / Client]
       │
       ▼ (HTTP Request: Method + URL + JSON Body)
[Django Root URLconf: config/urls.py]
       │
       ▼ (Dispatches /api/ to tickets/urls.py)
[DRF DefaultRouter: tickets/urls.py]
       │
       ▼ (Routes to TicketViewSet method)
[ViewSet: tickets/views.py]
       │
       ▼ (Deserializes and validates payload)
[Serializer: tickets/serializers.py]
       │
       ▼ (Valid data passed to ORM)
[Model: tickets/models.py]
       │
       ▼ (SQL Query executed)
[SQLite Database: db.sqlite3]
       │
       ▼ (Model instance returned)
[Serializer: tickets/serializers.py]
       │
       ▼ (Serializes Model to Python dictionary)
[DRF Response & Renderer]
       │
       ▼ (Formats JSON payload + HTTP Status Code)
[Postman / Client receives JSON Response]
```

### Purpose of Important Files

| File | Purpose |
|---|---|
| `config/settings.py` | Registers `rest_framework` and `tickets` apps, configures the database (`DATABASES`), and sets DRF filter backends and renderers. |
| `config/urls.py` | Master URL configuration that mounts the `admin/` route and delegates all `api/` endpoints to `tickets.urls`. |
| `tickets/models.py` | Defines the database schema for a `Ticket`, including fields, data types, status choices, constraints, and timestamps. |
| `tickets/serializers.py` | Translates complex model instances into JSON (and vice-versa), while enforcing strict field validation rules and custom error messages. |
| `tickets/views.py` | Contains `TicketViewSet`, which connects incoming HTTP requests to business logic, queryset filters, serializer validation, and HTTP responses. |
| `tickets/urls.py` | Uses DRF's `DefaultRouter` to automatically generate standard RESTful routes (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`, `update_status`). |
| `tickets/admin.py` | Configures the Django Admin dashboard with search bars, filters, and read-only timestamps. |
| `tickets/tests.py` | Houses the automated test suite to ensure endpoints, status codes, and validations behave properly without regression. |

---

## 5. Database Model: `Ticket`

The `Ticket` model stores support requests with the following schema:

| Field Name | Type | Description | Constraints / Behavior |
|---|---|---|---|
| `id` | `BigAutoField` | Unique primary key | Auto-incremented primary key. |
| `name` | `CharField` | Requester's full name | Required, max 100 characters, cannot be whitespace-only. |
| `email` | `EmailField` | Requester's email | Required, validated email format. |
| `title` | `CharField` | Ticket issue summary | Required, max 200 characters, cannot be whitespace-only. |
| `description` | `TextField` | Detailed problem description | Required, non-empty. |
| `status` | `CharField` | Current state of ticket | Choices: `'open'`, `'in_progress'`, `'resolved'`. Default: `'open'`. |
| `created_at` | `DateTimeField` | Creation timestamp | `auto_now_add=True`, set once on creation. |
| `updated_at` | `DateTimeField` | Last updated timestamp | `auto_now=True`, updated every time ticket is saved. |

---

## 6. Setup and Execution (Windows PowerShell Guide)

Follow these steps from the project root (`support_ticket/`):

### Step 1: Open Terminal in Project Directory
```powershell
# Verify you are in the support_ticket directory
Get-Location
```

### Step 2: Create a Virtual Environment (Optional if already created)
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
```powershell
# Standard activation
.\venv\Scripts\Activate.ps1
```

> **Note regarding PowerShell Execution Policy:**
> If you encounter `Execution_Policies` restriction error, you can either run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> .\venv\Scripts\Activate.ps1
> ```
> **Or run all commands directly using the virtual environment's Python executable without activating:**
> ```powershell
> .\venv\Scripts\python.exe -m pip install -r requirements.txt
> .\venv\Scripts\python.exe manage.py migrate
> .\venv\Scripts\python.exe manage.py test
> .\venv\Scripts\python.exe manage.py runserver
> ```

### Step 4: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 5: Apply Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create an Admin Superuser (Optional, for Admin Panel)
```powershell
python manage.py createsuperuser
```
Follow prompts to set username, email, and password.

### Step 7: Run Automated Tests
```powershell
python manage.py test
```
*Expected Output: `Ran 19 tests in 0.145s ... OK`*

### Step 8: Start the Development Server
```powershell
python manage.py runserver
```
The server will start at: `http://127.0.0.1:8000/`

---

## 7. REST API Endpoints & Postman Testing Guide

Base URL: `http://127.0.0.1:8000`

All requests sending data require the following HTTP Header:
```http
Content-Type: application/json
```

---

### Endpoint 1: Create a Ticket
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/api/tickets/`
- **Expected Status:** `201 Created`

#### Request Body (JSON)
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Cannot reset password",
  "description": "Clicking the reset link redirects to an expired token page."
}
```

#### Successful Response (`201 Created`)
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Cannot reset password",
  "description": "Clicking the reset link redirects to an expired token page.",
  "status": "open",
  "created_at": "2026-10-13T13:48:39.091332Z",
  "updated_at": "2026-10-13T13:48:39.091522Z"
}
```

---

### Endpoint 2: List All Tickets (with Filtering & Search)
- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/api/tickets/`
- **Expected Status:** `200 OK`

#### Query Parameters (Optional)
- Filter by status: `GET http://127.0.0.1:8000/api/tickets/?status=open`
- Search keyword: `GET http://127.0.0.1:8000/api/tickets/?search=password`
- Combined: `GET http://127.0.0.1:8000/api/tickets/?status=open&search=Jane`

#### Successful Response (`200 OK`)
```json
[
  {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "title": "Cannot reset password",
    "description": "Clicking the reset link redirects to an expired token page.",
    "status": "open",
    "created_at": "2026-10-13T13:48:39.091332Z",
    "updated_at": "2026-10-13T13:48:39.091522Z"
  }
]
```

---

### Endpoint 3: Retrieve a Single Ticket
- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/api/tickets/1/`
- **Expected Status:** `200 OK`

#### Successful Response (`200 OK`)
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Cannot reset password",
  "description": "Clicking the reset link redirects to an expired token page.",
  "status": "open",
  "created_at": "2026-10-13T13:48:39.091332Z",
  "updated_at": "2026-10-13T13:48:39.091522Z"
}
```

---

### Endpoint 4: Fully Update a Ticket (PUT)
- **Method:** `PUT`
- **URL:** `http://127.0.0.1:8000/api/tickets/1/`
- **Expected Status:** `200 OK`

#### Request Body (All required fields must be supplied)
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Cannot reset password - Resolved with manual link",
  "description": "Sent new token link directly to customer email.",
  "status": "resolved"
}
```

#### Successful Response (`200 OK`)
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Cannot reset password - Resolved with manual link",
  "description": "Sent new token link directly to customer email.",
  "status": "resolved",
  "created_at": "2026-10-13T13:48:39.091332Z",
  "updated_at": "2026-10-13T13:55:12.189421Z"
}
```

---

### Endpoint 5: Partially Update a Ticket (PATCH)
- **Method:** `PATCH`
- **URL:** `http://127.0.0.1:8000/api/tickets/1/`
- **Expected Status:** `200 OK`

#### Request Body (Only fields you want to update)
```json
{
  "title": "Updated Ticket Subject Only"
}
```

#### Successful Response (`200 OK`)
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Updated Ticket Subject Only",
  "description": "Sent new token link directly to customer email.",
  "status": "resolved",
  "created_at": "2026-10-13T13:48:39.091332Z",
  "updated_at": "2026-10-13T13:56:45.342119Z"
}
```

---

### Endpoint 6: Update Ticket Status (Custom Action)
- **Method:** `PATCH` (or `POST`)
- **URL:** `http://127.0.0.1:8000/api/tickets/1/update_status/`
- **Expected Status:** `200 OK`

#### Request Body (Valid choices: `open`, `in_progress`, `resolved`)
```json
{
  "status": "in_progress"
}
```

#### Successful Response (`200 OK`)
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "title": "Updated Ticket Subject Only",
  "description": "Sent new token link directly to customer email.",
  "status": "in_progress",
  "created_at": "2026-10-13T13:48:39.091332Z",
  "updated_at": "2026-10-13T13:57:30.984123Z"
}
```

---

### Endpoint 7: Delete a Ticket
- **Method:** `DELETE`
- **URL:** `http://127.0.0.1:8000/api/tickets/1/`
- **Expected Status:** `204 No Content`
- **Response Body:** *(Empty)*

---

## 8. Error Responses & Validation Handling

The API enforces strict validation and provides readable, field-specific error messages.

### Example A: Missing Required Fields
- **Request:** `POST http://127.0.0.1:8000/api/tickets/` with `{}`
- **Status:** `400 Bad Request`
```json
{
  "name": ["Name is required."],
  "email": ["Email is required."],
  "title": ["Title is required."],
  "description": ["Description is required."]
}
```

### Example B: Invalid Email Format
- **Request:** `POST http://127.0.0.1:8000/api/tickets/` with `"email": "invalid-email-address"`
- **Status:** `400 Bad Request`
```json
{
  "email": ["Enter a valid email address."]
}
```

### Example C: Blank or Whitespace-Only Field
- **Request:** `POST http://127.0.0.1:8000/api/tickets/` with `"name": "   "`
- **Status:** `400 Bad Request`
```json
{
  "name": ["Name cannot be blank or contain only whitespace."]
}
```

### Example D: Invalid Status in `update_status`
- **Request:** `PATCH http://127.0.0.1:8000/api/tickets/1/update_status/` with `{"status": "closed"}`
- **Status:** `400 Bad Request`
```json
{
  "status": ["Invalid status. Allowed choices are: open, in_progress, resolved."]
}
```

### Example E: Nonexistent Ticket (404)
- **Request:** `GET http://127.0.0.1:8000/api/tickets/99999/`
- **Status:** `404 Not Found`
```json
{
  "detail": "No Ticket matches the given query."
}
```

---

## 9. Rationale for HTTP Status Codes

| Status Code | Reason for Selection |
|---|---|
| **200 OK** | Used for successful retrieval (`GET`), full updates (`PUT`), partial updates (`PATCH`), and custom status modifications (`PATCH /update_status/`). Indicates request succeeded and returns the updated representation. |
| **201 Created** | Returned by `POST /api/tickets/` when a new ticket is successfully validated and stored in the database. |
| **204 No Content** | Returned by `DELETE /api/tickets/{id}/`. The resource was permanently deleted and there is no response body to return. |
| **400 Bad Request** | Returned when client-supplied input fails validation (missing fields, blank strings, invalid email format, invalid status choice). Returns clear field-level error messages. |
| **404 Not Found** | Returned when requesting, updating, or deleting a ticket ID that does not exist in the database. Prevents leaking internal state. |
| **500 Internal Server Error** | Should never occur during standard operation; caught and prevented by DRF exception handlers to keep internal stack traces secure. |
