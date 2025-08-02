from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Task

@shared_task
def check_and_notify_overdue_tasks():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(deadline__lt=now, completed=False)

    for task in overdue_tasks:
        subject = "Overdue Task Notification"
        message = (
            f"Hello {task.user.username},\n\n"
            f"Your task '{task.title}' was due on {task.deadline.strftime('%Y-%m-%d %H:%M:%S')} "
            f"and is now marked as overdue.\n\n"
            "Please take action as soon as possible."
        )
        send_mail(subject, message, "noreply@yourdomain.com", [task.user.email])

@shared_task
def send_overdue_reminders():
    from django.utils import timezone
    from .models import Task
    from django.core.mail import send_mail

    now = timezone.now()
    overdue_tasks = Task.objects.filter(deadline__lt=now, completed=False)

    for task in overdue_tasks:
        send_mail(
            subject="Overdue Task Reminder",
            message=f"Your task '{task.title}' is overdue!",
            from_email="admin@example.com",
            recipient_list=[task.user.email],
        )

