# AirlineCustomerSupport\models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('support', 'Support Agent'),
        ('admin', 'System Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    staff_id = models.CharField(max_length=6, blank=True, null=True)  # for agents only

    def is_customer(self):
        return self.role == 'customer'

    def is_support_agent(self):
        return self.role == 'support'

    def is_admin(self):
        return self.role == 'admin'

import uuid

class SupportRequest(models.Model):
    ISSUE_TYPES = [
        ('airport', 'Airport Issue'),
        ('airline', 'Airline Issue'),
        ('system', 'System Issue'),
        ('general', 'General/Other'),
    ]
    STATUS_TYPES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_requests')
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPES)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    request_code = models.CharField(max_length=8, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = uuid.uuid4().hex[:8].upper()  # 8-character uppercase unique code
        super().save(*args, **kwargs)


class Message(models.Model):
    support_request = models.ForeignKey(SupportRequest, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
