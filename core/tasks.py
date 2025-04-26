from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task, PersonalToDoItem, Notification

@shared_task
def check_upcoming_deadlines():
    """
    Check for tasks with deadlines in the next 2 hours and create notifications.
    This task should be scheduled to run every 15 minutes.
    """
    # Get the time window (2 hours from now)
    time_window = timezone.now() + timedelta(hours=2)
    
    # Check organizational tasks
    upcoming_tasks = Task.objects.filter(
        deadline__lte=time_window,
        deadline__gt=timezone.now(),
        status='P'  # Pending tasks only
    )
    
    for task in upcoming_tasks:
        # Create notification for each assignee
        for assignee in task.assignees.all():
            Notification.objects.create(
                user=assignee,
                title=f"Upcoming Deadline: {task.title}",
                message=f"The task '{task.title}' in {task.organization.name} is due in 2 hours.",
                task=task,
                reminder_type='deadline'
            )
    
    # Check personal tasks
    upcoming_personal_tasks = PersonalToDoItem.objects.filter(
        deadline__lte=time_window,
        deadline__gt=timezone.now(),
        completed=False
    )
    
    for task in upcoming_personal_tasks:
        Notification.objects.create(
            user=task.user,
            title=f"Upcoming Deadline: {task.title}",
            message=f"Your personal task '{task.title}' is due in 2 hours.",
            personal_task=task,
            reminder_type='deadline'
        )

@shared_task
def check_overdue_tasks():
    """
    Check for overdue tasks and create notifications.
    This task should be scheduled to run every hour.
    """
    # Get overdue tasks
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status='P'  # Pending tasks only
    )
    
    for task in overdue_tasks:
        # Create notification for each assignee
        for assignee in task.assignees.all():
            Notification.objects.create(
                user=assignee,
                title=f"Overdue Task: {task.title}",
                message=f"The task '{task.title}' in {task.organization.name} is overdue.",
                task=task,
                reminder_type='overdue'
            )
    
    # Check personal tasks
    overdue_personal_tasks = PersonalToDoItem.objects.filter(
        deadline__lt=timezone.now(),
        completed=False
    )
    
    for task in overdue_personal_tasks:
        Notification.objects.create(
            user=task.user,
            title=f"Overdue Task: {task.title}",
            message=f"Your personal task '{task.title}' is overdue.",
            personal_task=task,
            reminder_type='overdue'
        ) 