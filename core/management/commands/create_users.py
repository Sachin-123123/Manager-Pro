from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Creates 15 test users'

    def handle(self, *args, **kwargs):
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'password': 'testpass123'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'testpass123'},
            {'username': 'mike_johnson', 'email': 'mike@example.com', 'password': 'testpass123'},
            {'username': 'sarah_williams', 'email': 'sarah@example.com', 'password': 'testpass123'},
            {'username': 'david_brown', 'email': 'david@example.com', 'password': 'testpass123'},
            {'username': 'emma_davis', 'email': 'emma@example.com', 'password': 'testpass123'},
            {'username': 'james_wilson', 'email': 'james@example.com', 'password': 'testpass123'},
            {'username': 'lisa_moore', 'email': 'lisa@example.com', 'password': 'testpass123'},
            {'username': 'robert_taylor', 'email': 'robert@example.com', 'password': 'testpass123'},
            {'username': 'anna_anderson', 'email': 'anna@example.com', 'password': 'testpass123'},
            {'username': 'peter_thomas', 'email': 'peter@example.com', 'password': 'testpass123'},
            {'username': 'mary_jackson', 'email': 'mary@example.com', 'password': 'testpass123'},
            {'username': 'william_white', 'email': 'william@example.com', 'password': 'testpass123'},
            {'username': 'elizabeth_harris', 'email': 'elizabeth@example.com', 'password': 'testpass123'},
            {'username': 'charles_martin', 'email': 'charles@example.com', 'password': 'testpass123'},
        ]

        for user_data in users_data:
            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created user "{user.username}"'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'User "{user_data["username"]}" already exists')) 