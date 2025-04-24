# Airline Customer Support System

## HOSTED ON RENDER: https://airlinecustomerservice2025.onrender.com/login/

This is a Django-based web application for managing airline customer support requests. It supports three user roles:

- **Customers**: Submit and chat about support issues.
- **Support Agents**: Respond to requests, update statuses, and escalate issues.
- **Admins**: Oversee users, messages, and system operations.

---

## Features

- Secure user authentication and role-based dashboards
- Customers can submit support requests and chat with agents
- Support agents can manage and respond to chats
- Admins can create users and manage all support activity
- Live chat with status updates and escalation handling

---

## Setup

1. **Clone the repository**
    bash
    git clone <your-repo-url>
    cd <project-folder>

2. Run migrations
    python manage.py makemigrations
    python manage.py migrate

3. Create superuser
    python manage.py createsuperuser

4. Run server
    py manage.py runserver

5. Optionally you can add fixtures
    **users:** python manage.py loaddata AirlineCustomerSupport/fixtures/users.json
    **request:** python manage.py loaddata AirlineCustomerSupport/fixtures/support_requests.json
    **messages:** python manage.py loaddata AirlineCustomerSupport/fixtures/messages.json
