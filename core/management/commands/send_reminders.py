from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Task, ReminderLog
from core.email_service import send_task_reminder_email

class Command(BaseCommand):
    help = 'Send reminder emails for overdue tasks to users'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        overdue_tasks = Task.objects.filter(
            completed=False,
            reminder=True,
            deadline__lt=now
        )

        if not overdue_tasks.exists():
            self.stdout.write("No overdue tasks to send reminders for.")
            return

        for task in overdue_tasks:
            success = send_task_reminder_email(
                user_email=task.user.email,
                user_name=task.user.username,
                task_title=task.title,
                task_deadline=task.deadline
            )
            ReminderLog.objects.create(
                task=task,
                sent_at=now,
                reminder_type='email',
                status='sent' if success else 'failed',
                message='Overdue reminder email automatically sent.'
            )

        self.stdout.write(f"{overdue_tasks.count()} reminder(s) attempted.")
