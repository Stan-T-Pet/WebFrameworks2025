from django.core.management.base import BaseCommand
from AirlineCustomerSupport.models import CustomUser

class Command(BaseCommand):
    help = "Seed the database with test users: admin, support, and customer"

    def handle(self, *args, **options):
        users = [
            {
                'username': 'admin8',
                'email': 'admin8@mail.com',
                'password': 'admin123',
                'role': 'admin',
                'staff_id': '888888',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'support1',
                'email': 'support1@mail.com',
                'password': 'support123',
                'role': 'support',
                'staff_id': '222222',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'customer1',
                'email': 'customer1@mail.com',
                'password': 'customer123',
                'role': 'customer',
                'staff_id': None,
                'is_staff': False,
                'is_superuser': False
            },
        ]

        for user_data in users:
            if not CustomUser.objects.filter(username=user_data['username']).exists():
                user = CustomUser.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role'],
                    staff_id=user_data['staff_id']
                )
                user.is_staff = user_data['is_staff']
                user.is_superuser = user_data['is_superuser']
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {user_data['username']}"))
