from django.test import TestCase
from AirlineCustomerSupport.models import CustomUser

class UserRoleTest(TestCase):
    def setUp(self):
        # Create a customer
        CustomUser.objects.create_user(
            username='test_customer',
            email='customer@test.com',
            password='pass1234!',
            role='customer'
        )

        # Create a support agent
        CustomUser.objects.create_user(
            username='test_support',
            email='support@test.com',
            password='pass1234!',
            role='support',
            staff_id='111111'
        )

        # Create an admin
        CustomUser.objects.create_user(
            username='test_admin',
            email='admin@test.com',
            password='pass1234!',
            role='admin',
            staff_id='222222'
        )

    def test_customer_created(self):
        customer = CustomUser.objects.get(username='test_customer')
        self.assertEqual(customer.role, 'customer')
        self.assertIsNone(customer.staff_id)

    def test_support_created(self):
        support = CustomUser.objects.get(username='test_support')
        self.assertEqual(support.role, 'support')
        self.assertEqual(support.staff_id, '111111')

    def test_admin_created(self):
        admin = CustomUser.objects.get(username='test_admin')
        self.assertEqual(admin.role, 'admin')
        self.assertEqual(admin.staff_id, '222222')
