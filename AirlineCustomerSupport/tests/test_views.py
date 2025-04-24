from django.test import TestCase, Client
from django.urls import reverse
from AirlineCustomerSupport.models import CustomUser, SupportRequest, Message
from django.utils.crypto import get_random_string

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = CustomUser.objects.create_user(
            username='user1', email='user1@user1.com', password='password', role='customer')
        self.support = CustomUser.objects.create_user(
            username='support1', email='support1@support.com', password='password', role='support', staff_id='123456')
        self.admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@admin.com', password='password', role='admin', staff_id='999999')

        self.ticket = SupportRequest.objects.create(
            customer=self.customer,
            issue_type='general',
            subject='Test Subject',
            description='Test Description',
            request_code=get_random_string(8)
        )

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_customer_dashboard(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_support_request(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('support_request'))
        self.assertEqual(response.status_code, 200)

    def test_customer_messages(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('customer_messages'))
        self.assertEqual(response.status_code, 200)

    def test_customer_chat(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('customer_chat', kwargs={'request_code': self.ticket.request_code}))
        self.assertEqual(response.status_code, 200)

    def test_support_dashboard(self):
        self.client.login(username='support1', password='password')
        response = self.client.get(reverse('support_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_agent_message_list(self):
        self.client.login(username='support1', password='password')
        response = self.client.get(reverse('agent_messages'))
        self.assertEqual(response.status_code, 200)

    def test_support_chat(self):
        self.client.login(username='support1', password='password')
        response = self.client.get(reverse('support_chat', kwargs={'request_code': self.ticket.request_code}))
        self.assertEqual(response.status_code, 200)

    def test_support_elevator(self):
        self.client.login(username='support1', password='password')
        response = self.client.get(reverse('support_elevator', kwargs={'request_code': self.ticket.request_code}))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_chat_manager(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('chat_manager'))
        self.assertEqual(response.status_code, 200)

    def test_user_manager(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('user_manager'))
        self.assertEqual(response.status_code, 200)

    def test_manual_user_create(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('manual_user_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_user(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('view_user', kwargs={'user_id': self.customer.id}))
        self.assertEqual(response.status_code, 200)

    def test_edit_user(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_user', kwargs={'user_id': self.customer.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('delete_user', kwargs={'user_id': self.customer.id}))
        self.assertEqual(response.status_code, 200)
