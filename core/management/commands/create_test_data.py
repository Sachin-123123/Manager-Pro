from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import Organization, Task, Membership
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Creates test organizations, memberships, and tasks'

    def handle(self, *args, **kwargs):
        # Create organizations
        organizations_data = [
            {
                'name': 'Tech Solutions Inc.',
                'description': 'Leading technology solutions provider',
                'manager_username': 'john_doe',
                'members': ['jane_smith', 'mike_johnson', 'sarah_williams'],
                'tasks': [
                    {'title': 'Implement new API', 'description': 'Create REST API for client portal', 'priority': 'H'},
                    {'title': 'Update documentation', 'description': 'Update API documentation', 'priority': 'M'},
                    {'title': 'Fix UI bugs', 'description': 'Resolve reported UI issues', 'priority': 'L'},
                ]
            },
            {
                'name': 'Marketing Pro',
                'description': 'Digital marketing agency',
                'manager_username': 'jane_smith',
                'members': ['david_brown', 'emma_davis', 'james_wilson'],
                'tasks': [
                    {'title': 'Create social media campaign', 'description': 'Design campaign for new product', 'priority': 'H'},
                    {'title': 'Update website content', 'description': 'Refresh website with new content', 'priority': 'M'},
                    {'title': 'Analyze campaign metrics', 'description': 'Review and report on campaign performance', 'priority': 'L'},
                ]
            },
            {
                'name': 'Design Studio',
                'description': 'Creative design agency',
                'manager_username': 'mike_johnson',
                'members': ['lisa_moore', 'robert_taylor', 'anna_anderson'],
                'tasks': [
                    {'title': 'Design new logo', 'description': 'Create new brand identity', 'priority': 'H'},
                    {'title': 'Create marketing materials', 'description': 'Design brochures and flyers', 'priority': 'M'},
                    {'title': 'Update portfolio', 'description': 'Add new projects to website', 'priority': 'L'},
                ]
            }
        ]

        for org_data in organizations_data:
            try:
                # Create organization
                manager = User.objects.get(username=org_data['manager_username'])
                organization = Organization.objects.create(
                    name=org_data['name'],
                    description=org_data['description'],
                    manager=manager
                )
                self.stdout.write(self.style.SUCCESS(f'Created organization: {organization.name}'))

                # Create manager membership
                Membership.objects.create(
                    user=manager,
                    organization=organization,
                    role='M'
                )

                # Add members
                for member_username in org_data['members']:
                    try:
                        member = User.objects.get(username=member_username)
                        Membership.objects.create(
                            user=member,
                            organization=organization,
                            role='m'
                        )
                        self.stdout.write(self.style.SUCCESS(f'Added member {member.username} to {organization.name}'))
                    except User.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'User {member_username} not found'))
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(f'Membership already exists for {member_username}'))

                # Create tasks
                for task_data in org_data['tasks']:
                    task = Task.objects.create(
                        title=task_data['title'],
                        description=task_data['description'],
                        deadline=timezone.now() + timedelta(days=7),
                        priority=task_data['priority'],
                        status='P',
                        organization=organization
                    )
                    # Assign task to some members
                    for member_username in org_data['members'][:2]:  # Assign to first two members
                        try:
                            member = User.objects.get(username=member_username)
                            task.assignees.add(member)
                        except User.DoesNotExist:
                            continue
                    self.stdout.write(self.style.SUCCESS(f'Created task: {task.title}'))

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Manager {org_data["manager_username"]} not found'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'Organization {org_data["name"]} already exists')) 